"""
SusaGPT — ONNX Export
Cross-platform deployment: Windows, Linux, macOS, Android, iOS

Usage:
  python susagpt/export_onnx.py

Output:
  artifacts/models/SusaGPT.onnx            (full precision)
  artifacts/models/SusaGPT_quantized.onnx  (INT8 quantized, smaller)
"""

import sys
from pathlib import Path

# Allow running from project root
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import torch
from susagpt.src.config import BASE_MODEL_PATH, FINETUNED_MODEL_PATH, RLHF_MODEL_PATH, MODELS_DIR
from susagpt.src.model import SusaGPT

MODELS_DIR.mkdir(parents=True, exist_ok=True)


def load_model():
    # Load best available model
    path = None
    if RLHF_MODEL_PATH.exists():
        path = RLHF_MODEL_PATH
    elif FINETUNED_MODEL_PATH.exists():
        path = FINETUNED_MODEL_PATH
    elif BASE_MODEL_PATH.exists():
        path = BASE_MODEL_PATH
    else:
        print("❌  No trained model found. Run training scripts first.")
        sys.exit(1)

    print(f"✅  Loading model from: {path.name}")
    ckpt = torch.load(path, map_location="cpu", weights_only=False)
    model = SusaGPT(
        vocab_size   = ckpt["vocab_size"],
        embed_dim    = ckpt["embed_dim"],
        num_heads    = ckpt["num_heads"],
        num_kv_heads = ckpt.get("num_kv_heads", ckpt["num_heads"]),
        num_layers   = ckpt["num_layers"],
        max_len      = ckpt.get("max_len", 64),
        dropout      = 0.0,
    )
    model.load_state_dict(ckpt["model_state"])
    model.eval()
    print(f"   Parameters: {sum(p.numel() for p in model.parameters()):,}")
    return model, ckpt


def export_onnx(model, max_len=64):
    onnx_path = MODELS_DIR / "SusaGPT.onnx"
    dummy_input = torch.randint(0, 100, (1, max_len), dtype=torch.long)

    print(f"Exporting ONNX to: {onnx_path}")
    torch.onnx.export(
        model,
        (dummy_input,),
        str(onnx_path),
        export_params=True,
        opset_version=17,
        do_constant_folding=True,
        input_names=["input_ids"],
        output_names=["logits"],
        dynamic_axes={
            "input_ids": {0: "batch_size", 1: "seq_len"},
            "logits":    {0: "batch_size", 1: "seq_len"},
        },
    )
    size_mb = onnx_path.stat().st_size / 1024 / 1024
    print(f"✅  ONNX exported: {size_mb:.2f} MB → {onnx_path}")
    return onnx_path


def quantize_onnx(onnx_path):
    """INT8 quantize the ONNX model for mobile/edge deployment."""
    try:
        from onnxruntime.quantization import quantize_dynamic, QuantType
        quantized_path = MODELS_DIR / "SusaGPT_quantized.onnx"
        quantize_dynamic(
            str(onnx_path),
            str(quantized_path),
            weight_type=QuantType.QInt8,
        )
        orig_mb = onnx_path.stat().st_size / 1024 / 1024
        quant_mb = quantized_path.stat().st_size / 1024 / 1024
        print(f"✅  INT8 Quantized: {orig_mb:.2f} MB → {quant_mb:.2f} MB ({100*(1-quant_mb/orig_mb):.0f}% smaller)")
        return quantized_path
    except ImportError:
        print("⚠️  onnxruntime not installed. Run: pip install onnxruntime")
        return None
    except Exception as e:
        print(f"⚠️  Quantization skipped: {e}")
        return None


def verify_onnx(onnx_path, model, max_len=32):
    """Verify ONNX output matches PyTorch output."""
    try:
        import onnxruntime as ort
        import numpy as np

        session = ort.InferenceSession(str(onnx_path))
        dummy = torch.randint(0, 100, (1, max_len), dtype=torch.long)

        with torch.no_grad():
            pt_out = model(dummy).numpy()
        ort_out = session.run(["logits"], {"input_ids": dummy.numpy()})[0]

        max_diff = abs(pt_out - ort_out).max()
        print(f"✅  ONNX verification: max diff = {max_diff:.6f} ({'PASS' if max_diff < 1e-3 else 'FAIL'})")
    except ImportError:
        print("⚠️  onnxruntime not available for verification.")


def main():
    model, ckpt = load_model()
    onnx_path = export_onnx(model, max_len=ckpt.get("max_len", 64))
    verify_onnx(onnx_path, model)
    quantize_onnx(onnx_path)

    print("\n" + "="*50)
    print("ONNX Export Complete!")
    print("Files in artifacts/models/:")
    for f in (MODELS_DIR).glob("*.onnx"):
        print(f"  {f.name}  ({f.stat().st_size/1024/1024:.2f} MB)")
    print("\nTo run on any platform:")
    print("  pip install onnxruntime")
    print("  Use: onnxruntime.InferenceSession('SusaGPT.onnx')")


if __name__ == "__main__":
    main()
