from pathlib import Path


# config.py ka kaam project ke important knobs ek jagah rakhna hai.
# Isse baar-baar alag files me same numbers hardcode nahi karne padte.

BASE_DIR = Path(__file__).resolve().parent

DATA_PATH = BASE_DIR / "data.txt"
TOKENIZER_PATH = BASE_DIR / "tokenizer.json"
BASE_MODEL_PATH = BASE_DIR / "SusaGPT.pt"
FINETUNED_MODEL_PATH = BASE_DIR / "SusaGPT-finetuned.pt"
RLHF_MODEL_PATH = BASE_DIR / "SusaGPT-rlhf.pt"
QUANTIZED_MODEL_PATH = BASE_DIR / "SusaGPT-int8.pt"
QA_DATA_PATH = BASE_DIR / "qa_pairs.json"
PREFERENCE_DATA_PATH = BASE_DIR / "preference_pairs.json"


# Model architecture config:
# yahin se decide hota hai kitna choda model hoga.
MODEL_CONFIG = {
    "embed_dim": 64,
    "num_heads": 4,
    "num_kv_heads": 2,
    "num_layers": 2,
    "max_len": 32,
    "dropout": 0.1,
}


# Byte-level BPE tokenizer config:
# 256 base bytes ke upar merges add hote hain.
TOKENIZER_CONFIG = {
    "target_vocab_size": 768,
}


# Base pretraining ke liye config.
TRAIN_CONFIG = {
    "batch_size": 16,
    "epochs": 40,
    "learning_rate": 3e-4,
    "weight_decay": 0.01,
    "max_grad_norm": 1.0,
    "warmup_ratio": 0.1,
    "train_split": 0.8,
    "patience": 5,
    "gradient_accumulation_steps": 2,
    "mixed_precision": True,
}


# Fine-tuning me learning rate usually base training se chhota rakhte hain.
FINE_TUNE_CONFIG = {
    "batch_size": 8,
    "epochs": 30,
    "learning_rate": 1e-4,
    "weight_decay": 0.01,
    "max_grad_norm": 1.0,
    "warmup_ratio": 0.1,
    "train_split": 0.9,
    "patience": 5,
    "gradient_accumulation_steps": 2,
    "mixed_precision": True,
}


# RLHF-style alignment ke liye thoda aur gentle update rate rakhna better hota hai.
RLHF_CONFIG = {
    "epochs": 10,
    "learning_rate": 5e-5,
    "weight_decay": 0.0,
    "max_grad_norm": 1.0,
    "beta": 0.1,
}


# Generation sampling config:
# yahin se randomness aur answer quality ka balance control hota hai.
GENERATION_CONFIG = {
    "max_new_words": 30,
    "temperature": 0.8,
    "top_k": 25,
    "top_p": 0.9,
    "repetition_penalty": 1.1,
    "beam_width": 3,
    "use_kv_cache": True,
    "sampling_mode": "topk_topp",
    "mirostat_tau": 5.0,
    "mirostat_eta": 0.1,
}


# API config:
# FastAPI server ko kis host aur port par chalana hai.
API_CONFIG = {
    "host": "127.0.0.1",
    "port": 8000,
}
