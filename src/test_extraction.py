import fitz  # PyMuPDF
import pandas as pd
import os

def rect_overlaps(r1, r2):
    # Check if rectangle r1 overlaps with r2
    # Coordinates format: (x0, y0, x1, y1)
    return not (r1[2] < r2[0] or r1[0] > r2[2] or r1[3] < r2[1] or r1[1] > r2[3])

def extract_page_with_tables(page):
    # Find all tables on the page
    try:
        tables_obj = page.find_tables()
        tables = tables_obj.tables
    except Exception as e:
        # Fallback if find_tables is not supported or errors
        print(f"Table detection warning: {e}")
        tables = []

    # Get all text blocks
    # Each block is a tuple: (x0, y0, x1, y1, "text", block_no, block_type)
    blocks = page.get_text("blocks")
    
    # We will combine text blocks and tables, and sort them vertically (by y0)
    elements = []
    
    # Keep track of which tables we have processed
    table_bboxes = []
    for t in tables:
        table_bboxes.append(t.bbox)
        # Convert table to markdown
        df = t.to_pandas()
        # Clean column names and cell values (replace newlines with spaces)
        df.columns = [str(c).replace('\n', ' ').strip() for c in df.columns]
        for col in df.columns:
            df[col] = df[col].apply(lambda x: str(x).replace('\n', ' ').strip() if pd.notna(x) else "")
        
        # Build markdown table
        markdown_table = df.to_markdown(index=False)
        elements.append({
            "type": "table",
            "y0": t.bbox[1],
            "content": markdown_table
        })
        
    for block in blocks:
        x0, y0, x1, y1, text, block_no, block_type = block
        text = text.strip()
        if not text:
            continue
            
        # Check if this block falls inside any table
        inside_table = False
        for bbox in table_bboxes:
            # If the block overlaps significantly with a table, skip it
            if rect_overlaps((x0, y0, x1, y1), bbox):
                inside_table = True
                break
                
        if not inside_table:
            elements.append({
                "type": "text",
                "y0": y0,
                "content": text
            })
            
    # Sort elements from top to bottom based on y0 coordinate
    elements.sort(key=lambda x: x["y0"])
    
    # Join the elements
    page_content = []
    for el in elements:
        page_content.append(el["content"])
        
    return "\n\n".join(page_content)

def test_extract(pdf_path):
    print(f"Opening sample: {pdf_path}")
    doc = fitz.open(pdf_path)
    print(f"Total Pages: {len(doc)}")
    
    # Extract first 2 pages for validation
    for page_num in range(min(2, len(doc))):
        print(f"\n================ PAGE {page_num + 1} ================")
        page_text = extract_page_with_tables(doc[page_num])
        print(page_text)

if __name__ == "__main__":
    sample_pdf = r"c:\Projects\MyLLM\pdfs\Union Territory Tax (Rate)\2017\11-2017_UTGST_Rate.pdf"
    if os.path.exists(sample_pdf):
        test_extract(sample_pdf)
    else:
        print(f"Error: Sample PDF not found at {sample_pdf}")
