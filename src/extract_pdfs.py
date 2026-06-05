"""
GST PDF Data Extraction Pipeline for LLM Training
===================================================
Extracts all PDF files from pdfs/ directory, preserving tables as Markdown,
text as clean paragraphs, with rich metadata per document.

Output:
  data_extraction_for_llm/
    raw/
      <year>/           -- Per-year plain text files
    jsonl/
      <year>.jsonl      -- Per-year JSONL corpus (best for LLM training)
    combined/
      all_corpus.txt    -- Single merged text file (for small LLMs)
      all_corpus.jsonl  -- Single merged JSONL  (for large/RAG pipelines)
    stats/
      extraction_stats.json -- Summary: total docs, tokens, tables found, errors
"""

import fitz          # PyMuPDF
import json
import os
import re
import hashlib
import time
import pandas as pd
from pathlib import Path
from datetime import datetime


# ────────────────────────────────────────────────────────────────────────────
# CONFIG
# ────────────────────────────────────────────────────────────────────────────

PROJECT_ROOT   = Path(__file__).resolve().parents[1]
PDFS_DIR       = PROJECT_ROOT / "pdfs"
OUTPUT_DIR     = PROJECT_ROOT / "data_extraction_for_llm"

RAW_DIR      = OUTPUT_DIR / "raw"
JSONL_DIR    = OUTPUT_DIR / "jsonl"
COMBINED_DIR = OUTPUT_DIR / "combined"
STATS_DIR    = OUTPUT_DIR / "stats"

# Minimum number of meaningful words required to keep a block of text
MIN_TEXT_WORDS = 5

# Page-footer patterns to remove (page numbers, gazette headers, etc.)
NOISE_PATTERNS = [
    r"^\d+\s*$",                                    # bare page number
    r"^\s*\[to be published.*?\]\s*$",              # gazette header
    r"^\s*F\.\s*No\..*$",                           # file numbers
    r"^\s*\(See rule.*\)\s*$",                      # bracket-only lines
    r"^\s*G\.S\.R\.\s*\(E\)\.?\s*$",              # gazette short headers
    r"^\s*www\.\S+\s*$",                            # bare URLs
]
NOISE_REGEX = [re.compile(p, re.IGNORECASE) for p in NOISE_PATTERNS]


# ────────────────────────────────────────────────────────────────────────────
# UTILITY HELPERS
# ────────────────────────────────────────────────────────────────────────────

def make_dirs():
    for d in [RAW_DIR, JSONL_DIR, COMBINED_DIR, STATS_DIR]:
        d.mkdir(parents=True, exist_ok=True)


def rect_overlaps(r1, r2):
    """Return True if two (x0,y0,x1,y1) rectangles overlap."""
    return not (r1[2] < r2[0] or r1[0] > r2[2] or r1[3] < r2[1] or r1[1] > r2[3])


def is_noise(line: str) -> bool:
    line = line.strip()
    if not line:
        return True
    for rx in NOISE_REGEX:
        if rx.match(line):
            return True
    return False


def clean_text(text: str) -> str:
    """Normalize whitespace, remove noise lines, collapse blank lines."""
    lines = text.splitlines()
    cleaned = []
    for line in lines:
        stripped = line.strip()
        if is_noise(stripped):
            continue
        # Replace multiple internal spaces with single space
        stripped = re.sub(r" {2,}", " ", stripped)
        cleaned.append(stripped)

    # Collapse 3+ consecutive blank lines into a single blank line
    result = "\n".join(cleaned)
    result = re.sub(r"\n{3,}", "\n\n", result)
    return result.strip()


def table_to_markdown(table) -> str:
    """Convert a PyMuPDF table object to a clean Markdown table string."""
    try:
        df = table.to_pandas()
        # Clean column headers
        df.columns = [str(c).replace("\n", " ").strip() for c in df.columns]
        # Clean cell values
        for col in df.columns:
            df[col] = df[col].apply(
                lambda x: re.sub(r"\s+", " ", str(x)).strip() if pd.notna(x) else ""
            )
        return df.to_markdown(index=False)
    except Exception as e:
        return f"[TABLE EXTRACTION ERROR: {e}]"


def word_count(text: str) -> int:
    return len(text.split())


def detect_language_hint(text: str) -> str:
    """
    Very lightweight heuristic language tag.
    For proper detection install langdetect; this covers the
    most common scripts found in Indian Government PDFs.
    """
    urdu_chars   = sum(1 for c in text if "\u0600" <= c <= "\u06FF")
    hindi_chars  = sum(1 for c in text if "\u0900" <= c <= "\u097F")
    total_chars  = max(len(text), 1)
    if urdu_chars / total_chars > 0.1:
        return "ur"
    if hindi_chars / total_chars > 0.1:
        return "hi"
    return "en"


# ────────────────────────────────────────────────────────────────────────────
# CORE EXTRACTION
# ────────────────────────────────────────────────────────────────────────────

def extract_single_page(page) -> tuple[str, int]:
    """
    Extract one PDF page, inserting Markdown tables in reading order.
    Returns (page_text, num_tables_found).
    """
    # ── Detect tables ────────────────────────────────────────────────────────
    try:
        tables_obj = page.find_tables()
        tables_list = tables_obj.tables
    except Exception:
        tables_list = []

    elements = []
    table_bboxes = []

    for t in tables_list:
        table_bboxes.append(t.bbox)
        md = table_to_markdown(t)
        elements.append({
            "y0": t.bbox[1],
            "type": "table",
            "content": md,
        })

    # ── Collect text blocks (skipping table regions) ─────────────────────────
    blocks = page.get_text("blocks")  # (x0,y0,x1,y1,text,block_no,type)
    for block in blocks:
        x0, y0, x1, y1, text, _, btype = block
        if btype != 0:          # skip image blocks
            continue
        text = text.strip()
        if not text:
            continue
        inside_table = any(rect_overlaps((x0, y0, x1, y1), tb) for tb in table_bboxes)
        if inside_table:
            continue
        elements.append({"y0": y0, "type": "text", "content": text})

    # ── Sort top-to-bottom ───────────────────────────────────────────────────
    elements.sort(key=lambda e: e["y0"])

    page_parts = [e["content"] for e in elements]
    raw_page = "\n\n".join(page_parts)
    return raw_page, len(tables_list)


def extract_pdf(pdf_path: Path) -> dict:
    """
    Extract a single PDF file.
    Returns a rich document dict ready for JSONL serialisation.
    """
    doc = fitz.open(str(pdf_path))

    pages_text = []
    total_tables = 0

    for page_num in range(len(doc)):
        page = doc[page_num]
        page_text, n_tables = extract_single_page(page)
        cleaned = clean_text(page_text)
        if cleaned:
            pages_text.append(cleaned)
        total_tables += n_tables

    doc.close()

    full_text = "\n\n".join(pages_text)

    # ── Build metadata ───────────────────────────────────────────────────────
    rel_path = pdf_path.relative_to(PDFS_DIR)
    parts = rel_path.parts   # e.g. ('Union Territory Tax (Rate)', '2017', 'file.pdf')

    category = parts[0] if len(parts) >= 1 else "Unknown"
    year     = parts[1] if len(parts) >= 2 else "Unknown"
    filename = pdf_path.name

    # Derive notification number from filename where possible
    notif_match = re.search(r"notfctn[_-]?(\d+)", filename, re.IGNORECASE)
    notif_num   = notif_match.group(1) if notif_match else None

    return {
        "id"           : hashlib.md5(str(pdf_path).encode()).hexdigest()[:12],
        "source_file"  : str(rel_path).replace("\\", "/"),
        "category"     : category,
        "year"         : year,
        "filename"     : filename,
        "notification" : notif_num,
        "language"     : detect_language_hint(full_text),
        "pages"        : len(pages_text),
        "tables_found" : total_tables,
        "word_count"   : word_count(full_text),
        "text"         : full_text,
    }


# ────────────────────────────────────────────────────────────────────────────
# MAIN PIPELINE
# ────────────────────────────────────────────────────────────────────────────

def run():
    make_dirs()
    start_time = time.time()

    # Collect all PDFs
    all_pdfs = sorted(PDFS_DIR.rglob("*.pdf"))
    total    = len(all_pdfs)
    print(f"Found {total} PDF files under {PDFS_DIR}\n")

    stats = {
        "generated_at"    : datetime.now().isoformat(),
        "total_pdfs"      : total,
        "success"         : 0,
        "errors"          : 0,
        "skipped_empty"   : 0,
        "total_words"     : 0,
        "total_tables"    : 0,
        "by_year"         : {},
        "error_files"     : [],
    }

    # Open combined output files
    combined_txt_path  = COMBINED_DIR / "all_corpus.txt"
    combined_jsonl_path = COMBINED_DIR / "all_corpus.jsonl"

    with (
        open(combined_txt_path,  "w", encoding="utf-8") as f_txt,
        open(combined_jsonl_path, "w", encoding="utf-8") as f_jsonl,
    ):
        for idx, pdf_path in enumerate(all_pdfs, 1):
            print(f"[{idx:4}/{total}] {pdf_path.relative_to(PDFS_DIR)}", end=" ... ", flush=True)

            try:
                doc_dict = extract_pdf(pdf_path)
            except Exception as e:
                print(f"ERROR: {e}")
                stats["errors"] += 1
                stats["error_files"].append({"file": str(pdf_path), "error": str(e)})
                continue

            if word_count(doc_dict["text"]) < MIN_TEXT_WORDS:
                print("SKIPPED (empty/no text)")
                stats["skipped_empty"] += 1
                continue

            year = doc_dict["year"]

            # ── Per-year RAW text ────────────────────────────────────────────
            year_raw_dir = RAW_DIR / year
            year_raw_dir.mkdir(parents=True, exist_ok=True)
            raw_txt_path = year_raw_dir / pdf_path.with_suffix(".txt").name
            raw_txt_path.write_text(doc_dict["text"], encoding="utf-8")

            # ── Per-year JSONL ───────────────────────────────────────────────
            year_jsonl_path = JSONL_DIR / f"{year}.jsonl"
            with open(year_jsonl_path, "a", encoding="utf-8") as jf:
                jf.write(json.dumps(doc_dict, ensure_ascii=False) + "\n")

            # ── Combined outputs ─────────────────────────────────────────────
            # Delimiter block so LLM training knows document boundaries
            separator = (
                f"\n\n{'='*80}\n"
                f"SOURCE: {doc_dict['source_file']}\n"
                f"CATEGORY: {doc_dict['category']} | YEAR: {year} | LANG: {doc_dict['language']}\n"
                f"{'='*80}\n\n"
            )
            f_txt.write(separator + doc_dict["text"] + "\n")
            f_jsonl.write(json.dumps(doc_dict, ensure_ascii=False) + "\n")

            # ── Update stats ─────────────────────────────────────────────────
            stats["success"]      += 1
            stats["total_words"]  += doc_dict["word_count"]
            stats["total_tables"] += doc_dict["tables_found"]

            yr_stats = stats["by_year"].setdefault(year, {"docs": 0, "words": 0, "tables": 0})
            yr_stats["docs"]   += 1
            yr_stats["words"]  += doc_dict["word_count"]
            yr_stats["tables"] += doc_dict["tables_found"]

            print(f"OK  ({doc_dict['word_count']:,} words, {doc_dict['tables_found']} tables)")

    # ── Write stats ──────────────────────────────────────────────────────────
    elapsed = round(time.time() - start_time, 1)
    stats["elapsed_seconds"] = elapsed

    stats_path = STATS_DIR / "extraction_stats.json"
    stats_path.write_text(json.dumps(stats, indent=2, ensure_ascii=False), encoding="utf-8")

    # ── Summary ──────────────────────────────────────────────────────────────
    print("\n" + "="*60)
    print("EXTRACTION COMPLETE")
    print("="*60)
    print(f"  Total PDFs     : {total}")
    print(f"  Successful     : {stats['success']}")
    print(f"  Errors         : {stats['errors']}")
    print(f"  Skipped (empty): {stats['skipped_empty']}")
    print(f"  Total words    : {stats['total_words']:,}")
    print(f"  Total tables   : {stats['total_tables']:,}")
    print(f"  Time taken     : {elapsed}s")
    print(f"\nOutputs saved to: {OUTPUT_DIR}")
    print(f"  Combined TXT   : {combined_txt_path}")
    print(f"  Combined JSONL : {combined_jsonl_path}")
    print(f"  Stats          : {stats_path}")


if __name__ == "__main__":
    run()
