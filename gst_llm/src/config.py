from pathlib import Path

# ─────────────────────────────────────────────────────────
# GST LLM — Config
# Yeh file GST-specific Tiny LLM ke saare settings rakhti hai.
# ─────────────────────────────────────────────────────────

PACKAGE_DIR   = Path(__file__).resolve().parent
PROJECT_ROOT  = PACKAGE_DIR.parent          # gst_llm/
DATA_DIR      = PROJECT_ROOT / "data"
ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"
MODELS_DIR    = ARTIFACTS_DIR / "models"
TOKENIZER_DIR = ARTIFACTS_DIR / "tokenizer"

# ── Data Paths ──────────────────────────────────────────
DATA_PATH           = DATA_DIR / "corpus.txt"          # GST pretraining corpus
QA_DATA_PATH        = DATA_DIR / "qa_pairs.json"       # Fine-tuning QA pairs
PREFERENCE_DATA_PATH= DATA_DIR / "preference_pairs.json"

# ── Artifact Paths ──────────────────────────────────────
TOKENIZER_PATH      = TOKENIZER_DIR / "tokenizer.json"
BASE_MODEL_PATH     = MODELS_DIR / "gst_llm_base.pt"
FINETUNED_MODEL_PATH= MODELS_DIR / "gst_llm_finetuned.pt"
RLHF_MODEL_PATH     = MODELS_DIR / "gst_llm_rlhf.pt"
QUANTIZED_MODEL_PATH= MODELS_DIR / "gst_llm_int8.pt"


# ── Model Architecture ──────────────────────────────────
# 176K words ka GST corpus hai isliye max_len aur embed_dim badhai hai.
# Phir bhi yeh ek Tiny LLM hai — CPU par bhi chalega.
#
# Parameters estimate:
#   embed_dim=128, num_layers=4 → ~2-3M params
#
MODEL_CONFIG = {
    "embed_dim"   : 64,     # Reduced for 1-2 min training
    "num_heads"   : 4,
    "num_kv_heads": 2,
    "num_layers"  : 2,      # Reduced for 1-2 min training
    "max_len"     : 64,      # Reduced for 1-2 min training
    "dropout"     : 0.1,
}


# ── Tokenizer ───────────────────────────────────────────
# Reduced for 1-2 min training
TOKENIZER_CONFIG = {
    "target_vocab_size": 1000,
}


# ── Base Pretraining ────────────────────────────────────
TRAIN_CONFIG = {
    "batch_size"                : 32,    # Increased batch size for faster vectorized training
    "epochs"                    : 6,     # Reduced epochs for ultra-fast training
    "learning_rate"             : 5e-4,
    "weight_decay"              : 0.01,
    "max_grad_norm"             : 1.0,
    "warmup_ratio"              : 0.1,
    "train_split"               : 0.9,
    "patience"                  : 3,     # Reduced patience for early stopping
    "gradient_accumulation_steps": 1,     # Single step for speed
    "mixed_precision"           : True,
}


# ── Fine-Tuning (QA Pairs) ──────────────────────────────
FINE_TUNE_CONFIG = {
    "batch_size"                : 8,
    "epochs"                    : 10,    # Reduced epochs
    "learning_rate"             : 1e-4,
    "weight_decay"              : 0.01,
    "max_grad_norm"             : 1.0,
    "warmup_ratio"              : 0.1,
    "train_split"               : 0.9,
    "patience"                  : 3,     # Reduced patience
    "gradient_accumulation_steps": 1,     # Single step
    "mixed_precision"           : True,
}


# ── RLHF Alignment ─────────────────────────────────────
RLHF_CONFIG = {
    "epochs"       : 5,     # Reduced epochs
    "learning_rate": 5e-5,
    "weight_decay" : 0.0,
    "max_grad_norm": 1.0,
    "beta"         : 0.1,
}


# ── Generation / Inference ──────────────────────────────
GENERATION_CONFIG = {
    "max_new_words"    : 80,       # GST answers thode lambe hote hain
    "temperature"      : 0.7,      # thoda conservative for factual answers
    "top_k"            : 30,
    "top_p"            : 0.9,
    "repetition_penalty": 1.15,
    "beam_width"       : 3,
    "use_kv_cache"     : True,
    "sampling_mode"    : "topk_topp",
    "mirostat_tau"     : 5.0,
    "mirostat_eta"     : 0.1,
}


# ── API Server ──────────────────────────────────────────
API_CONFIG = {
    "host": "127.0.0.1",
    "port": 8001,           # 8001 taaki main SusaGPT (8000) se conflict na ho
}
