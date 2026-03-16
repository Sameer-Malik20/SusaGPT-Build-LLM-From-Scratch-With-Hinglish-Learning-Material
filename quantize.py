import os

import torch

from config import QUANTIZED_MODEL_PATH
from generate import apply_dynamic_int8_quantization, load_everything, resolve_model_path


# quantize.py ka kaam trained model ko INT8 version me convert karna hai.
# Ye mostly CPU inference aur sharing ke liye useful hota hai.
# Important:
# Dynamic INT8 quantization inference-focused feature hai, training ke liye nahi.


def save_quantized_model(model, tokenizer, source_path, destination_path):
    torch.save(
        {
            "model_state": model.state_dict(),
            "vocab_size": tokenizer.vocab_size,
            "embed_dim": model.embed_dim,
            "num_heads": model.num_heads,
            "num_kv_heads": model.num_kv_heads,
            "num_layers": model.num_layers,
            "max_len": model.max_len,
            "dropout": model.dropout,
            "quantized": True,
            "source_model_path": str(source_path),
        },
        destination_path,
    )


if __name__ == "__main__":
    source_path = resolve_model_path(prefer_quantized=False)
    model, tokenizer, loaded_path = load_everything(
        model_path=source_path,
        prefer_quantized=False,
        return_path=True,
    )

    print(f"Source model -> {loaded_path}")

    # INT8 quantization ke baad Linear layers compact form me pack hoti hain.
    quantized_model = apply_dynamic_int8_quantization(model)
    save_quantized_model(
        model=quantized_model,
        tokenizer=tokenizer,
        source_path=loaded_path,
        destination_path=QUANTIZED_MODEL_PATH,
    )

    source_size_mb = os.path.getsize(loaded_path) / (1024 * 1024)
    quantized_size_mb = os.path.getsize(QUANTIZED_MODEL_PATH) / (1024 * 1024)

    print(f"INT8 model saved -> {QUANTIZED_MODEL_PATH}")
    print(f"Original size   -> {source_size_mb:.2f} MB")
    print(f"INT8 size       -> {quantized_size_mb:.2f} MB")
