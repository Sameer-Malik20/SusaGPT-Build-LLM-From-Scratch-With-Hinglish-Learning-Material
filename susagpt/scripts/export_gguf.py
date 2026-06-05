import sys
import json
from pathlib import Path
import torch
import numpy as np

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from gguf import GGUFWriter
from susagpt.src.config import RLHF_MODEL_PATH, TOKENIZER_PATH, MODELS_DIR

def export_to_gguf():
    model_path = RLHF_MODEL_PATH
    tokenizer_path = TOKENIZER_PATH
    gguf_out_path = MODELS_DIR / "susagpt.gguf"
    
    if not model_path.exists():
        print(f"❌ Checkpoint not found at: {model_path}")
        return
        
    print(f"Loading checkpoint: {model_path}")
    ckpt = torch.load(model_path, map_location="cpu", weights_only=False)
    state_dict = ckpt["model_state"]
    
    vocab_size = ckpt["vocab_size"]
    embed_dim = ckpt["embed_dim"]
    num_heads = ckpt["num_heads"]
    num_kv_heads = ckpt.get("num_kv_heads", num_heads)
    num_layers = ckpt["num_layers"]
    max_len = max(512, ckpt.get("max_len", 64))
    
    print(f"Model architecture loaded:")
    print(f" - Vocab size: {vocab_size}")
    print(f" - Embed dim: {embed_dim}")
    print(f" - Layers: {num_layers}")
    print(f" - Attention Heads: {num_heads} Query, {num_kv_heads} KV")
    print(f" - Context length: {max_len}")
    
    # Helper to convert byte sequence to GPT-2 compatible Unicode string
    def get_bytes_to_unicode_dict():
        bs = list(range(ord("!"), ord("~")+1)) + list(range(ord("¡"), ord("¬")+1)) + list(range(ord("®"), ord("ÿ")+1))
        cs = bs[:]
        n = 0
        for b in range(2**8):
            if b not in bs:
                bs.append(b)
                cs.append(2**8 + n)
                n += 1
        cs = [chr(n) for n in cs]
        return dict(zip(bs, cs))

    byte_encoder = get_bytes_to_unicode_dict()

    def map_bytes_to_gpt2_string(b_seq):
        return "".join(byte_encoder[b] for b in b_seq)

    # Load tokenizer details
    print(f"Loading tokenizer: {tokenizer_path}")
    with open(tokenizer_path, "r", encoding="utf-8") as f:
        tok_data = json.load(f)
        
    # Prepare tokens, scores, and types
    tokens = []
    scores = []
    tok_types = []
    
    for token_id in range(vocab_size):
        token_val = tok_data["tokens"].get(str(token_id))
        if token_id == tok_data["pad_token_id"]:
            tokens.append("<PAD>")
        else:
            token_bytes = bytes.fromhex(token_val)
            tokens.append(map_bytes_to_gpt2_string(token_bytes))
        scores.append(0.0)
        tok_types.append(1) # Normal tokens
        
    # Setup GGUFWriter
    print(f"Writing GGUF output to: {gguf_out_path}")
    writer = GGUFWriter(str(gguf_out_path), "llama")
    
    # Add metadata
    writer.add_architecture()
    writer.add_context_length(max_len)
    writer.add_embedding_length(embed_dim)
    writer.add_block_count(num_layers)
    writer.add_feed_forward_length(embed_dim * 4)
    writer.add_head_count(num_heads)
    writer.add_head_count_kv(num_kv_heads)
    writer.add_layer_norm_rms_eps(1e-6)
    
    # Add tokenizer details
    writer.add_tokenizer_model("gpt2")
    writer.add_token_list(tokens)
    writer.add_token_scores(scores)
    writer.add_token_types(tok_types)
    
    # Add merges if present
    merges = []
    for left_hex, right_hex, merged_hex in tok_data.get("merges", []):
        try:
            left_bytes = bytes.fromhex(left_hex)
            right_bytes = bytes.fromhex(right_hex)
            left_mapped = map_bytes_to_gpt2_string(left_bytes)
            right_mapped = map_bytes_to_gpt2_string(right_bytes)
            merges.append(f"{left_mapped} {right_mapped}")
        except Exception:
            pass
            
    if merges:
        writer.add_token_merges(merges)
        
    # Write tensors mapping PyTorch structure to LLaMA standard names
    for name, tensor in state_dict.items():
        arr = tensor.cpu().float().numpy()
        gguf_name = None
        
        if name == "embedding.embedding.weight":
            gguf_name = "token_embd.weight"
        elif name == "norm.weight":
            gguf_name = "output_norm.weight"
        elif name == "output.weight":
            gguf_name = "output.weight"
        elif name.startswith("blocks."):
            parts = name.split(".")
            layer_idx = parts[1]
            sub = parts[2]
            param_type = parts[-1]
            
            if sub == "norm1":
                gguf_name = f"blk.{layer_idx}.attn_norm.{param_type}"
            elif sub == "norm2":
                gguf_name = f"blk.{layer_idx}.ffn_norm.{param_type}"
            elif sub == "attention":
                proj = parts[3]
                if proj == "W_q":
                    gguf_name = f"blk.{layer_idx}.attn_q.{param_type}"
                elif proj == "W_k":
                    gguf_name = f"blk.{layer_idx}.attn_k.{param_type}"
                elif proj == "W_v":
                    gguf_name = f"blk.{layer_idx}.attn_v.{param_type}"
                elif proj == "W_o":
                    gguf_name = f"blk.{layer_idx}.attn_output.{param_type}"
            elif sub == "ff":
                layer_name = parts[3]
                if layer_name == "w1":
                    gguf_name = f"blk.{layer_idx}.ffn_gate.{param_type}"
                elif layer_name == "w2":
                    gguf_name = f"blk.{layer_idx}.ffn_down.{param_type}"
                elif layer_name == "w3":
                    gguf_name = f"blk.{layer_idx}.ffn_up.{param_type}"
                    
        if gguf_name:
            print(f"Adding tensor: {name} ➔ {gguf_name} (shape: {arr.shape})")
            writer.add_tensor(gguf_name, arr)
            
    # Finalize GGUF file
    writer.write_header_to_file()
    writer.write_kv_data_to_file()
    writer.write_tensors_to_file()
    writer.close()
    print(f"🎉 GGUF successfully created at: {gguf_out_path}")

if __name__ == "__main__":
    export_to_gguf()
