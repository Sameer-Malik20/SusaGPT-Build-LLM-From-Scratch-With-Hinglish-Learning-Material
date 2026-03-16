import math

import torch
import torch.nn as nn
import torch.nn.functional as F


# Is version me 3 major architecture upgrades hain:
# 1. SwiGLU activation
# 2. Grouped Query Attention (GQA)
# 3. RoPE + RMSNorm + Dropout support


class RMSNorm(nn.Module):
    # RMSNorm vector ke scale ko stable rakhta hai.
    # Ye LayerNorm se thoda simpler hota hai aur modern LLMs me kaafi common hai.
    def __init__(self, dim, eps=1e-6):
        super().__init__()
        self.eps = eps
        self.weight = nn.Parameter(torch.ones(dim))

    def forward(self, x):
        rms = torch.rsqrt(x.pow(2).mean(dim=-1, keepdim=True) + self.eps)
        return x * rms * self.weight


class RotaryEmbedding(nn.Module):
    # RoPE positional information ko attention ke andar inject karta hai.
    def __init__(self, dim, base=10000):
        super().__init__()
        inv_freq = 1.0 / (base ** (torch.arange(0, dim, 2).float() / dim))
        self.register_buffer("inv_freq", inv_freq)

    def get_cos_sin(self, seq_len, device, dtype, start_pos=0):
        positions = torch.arange(start_pos, start_pos + seq_len, device=device).float()
        freqs = torch.outer(positions, self.inv_freq)
        cos = torch.cos(freqs).to(dtype=dtype)
        sin = torch.sin(freqs).to(dtype=dtype)
        return cos.unsqueeze(0).unsqueeze(0), sin.unsqueeze(0).unsqueeze(0)


def rotate_half(x):
    x_even = x[..., ::2]
    x_odd = x[..., 1::2]
    rotated = torch.stack((-x_odd, x_even), dim=-1)
    return rotated.flatten(start_dim=-2)


def apply_rotary_pos_emb(q, k, cos, sin):
    cos = torch.repeat_interleave(cos, 2, dim=-1)
    sin = torch.repeat_interleave(sin, 2, dim=-1)
    q = (q * cos) + (rotate_half(q) * sin)
    k = (k * cos) + (rotate_half(k) * sin)
    return q, k


class EmbeddingLayer(nn.Module):
    def __init__(self, vocab_size, embed_dim):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)

    def forward(self, x):
        return self.embedding(x)


class SelfAttention(nn.Module):
    # GQA ka idea:
    # Query heads zyada ho sakte hain, lekin Key/Value heads kam rakhte hain.
    # Isse memory aur cache cost kam hoti hai.
    def __init__(self, embed_dim, num_heads, num_kv_heads, dropout=0.1):
        super().__init__()

        if embed_dim % num_heads != 0:
            raise ValueError("embed_dim must be divisible by num_heads")
        if num_heads % num_kv_heads != 0:
            raise ValueError("num_heads must be divisible by num_kv_heads")

        self.embed_dim = embed_dim
        self.num_heads = num_heads
        self.num_kv_heads = num_kv_heads
        self.head_dim = embed_dim // num_heads
        self.kv_repeat = num_heads // num_kv_heads

        self.W_q = nn.Linear(embed_dim, embed_dim)

        # GQA me K aur V ki width kam hoti hai kyunki inke heads kam hote hain.
        self.W_k = nn.Linear(embed_dim, num_kv_heads * self.head_dim)
        self.W_v = nn.Linear(embed_dim, num_kv_heads * self.head_dim)
        self.W_o = nn.Linear(embed_dim, embed_dim)

        self.attn_dropout = nn.Dropout(dropout)
        self.resid_dropout = nn.Dropout(dropout)
        self.rope = RotaryEmbedding(self.head_dim)

    def forward(self, x, layer_past=None, use_cache=False, start_pos=0):
        batch_size, time_steps, channels = x.shape

        queries = self.W_q(x)
        keys = self.W_k(x)
        values = self.W_v(x)

        queries = queries.view(
            batch_size, time_steps, self.num_heads, self.head_dim
        ).transpose(1, 2)
        keys = keys.view(
            batch_size, time_steps, self.num_kv_heads, self.head_dim
        ).transpose(1, 2)
        values = values.view(
            batch_size, time_steps, self.num_kv_heads, self.head_dim
        ).transpose(1, 2)

        cos, sin = self.rope.get_cos_sin(
            seq_len=time_steps,
            device=x.device,
            dtype=queries.dtype,
            start_pos=start_pos,
        )
        queries, keys = apply_rotary_pos_emb(queries, keys, cos, sin)

        if layer_past is not None:
            past_keys, past_values = layer_past
            keys = torch.cat([past_keys, keys], dim=2)
            values = torch.cat([past_values, values], dim=2)

        present = (keys, values) if use_cache else None

        # Query heads zyada hain aur KV heads kam.
        # Isliye K aur V ko repeat karke query-head count ke saath align karte hain.
        repeated_keys = keys.repeat_interleave(self.kv_repeat, dim=1)
        repeated_values = values.repeat_interleave(self.kv_repeat, dim=1)

        scale = math.sqrt(self.head_dim)
        scores = torch.matmul(queries, repeated_keys.transpose(-2, -1)) / scale

        total_kv_len = repeated_keys.size(2)
        if not (layer_past is not None and time_steps == 1):
            query_positions = torch.arange(
                start_pos, start_pos + time_steps, device=x.device
            ).unsqueeze(-1)
            key_positions = torch.arange(total_kv_len, device=x.device).unsqueeze(0)
            mask = key_positions > query_positions
            scores = scores.masked_fill(mask.unsqueeze(0).unsqueeze(0), float("-inf"))

        attention_weights = F.softmax(scores, dim=-1)
        attention_weights = self.attn_dropout(attention_weights)
        output = torch.matmul(attention_weights, repeated_values)

        output = output.transpose(1, 2).contiguous().view(
            batch_size, time_steps, channels
        )
        output = self.W_o(output)
        output = self.resid_dropout(output)
        return output, present


class SwiGLUFeedForward(nn.Module):
    # SwiGLU = Swish (SiLU) + GLU style gating.
    # LLaMA family me ye common pattern hai.
    # Idea simple hai:
    # ek branch gate banati hai, doosri branch content.
    # phir SiLU gate ke saath multiply karke controlled information flow milta hai.
    def __init__(self, embed_dim, dropout=0.1):
        super().__init__()
        hidden_dim = embed_dim * 4

        self.w1 = nn.Linear(embed_dim, hidden_dim, bias=False)
        self.w3 = nn.Linear(embed_dim, hidden_dim, bias=False)
        self.w2 = nn.Linear(hidden_dim, embed_dim, bias=False)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        gated = F.silu(self.w1(x)) * self.w3(x)
        output = self.w2(gated)
        return self.dropout(output)


class TransformerBlock(nn.Module):
    def __init__(self, embed_dim, num_heads, num_kv_heads, dropout=0.1):
        super().__init__()
        self.attention = SelfAttention(
            embed_dim=embed_dim,
            num_heads=num_heads,
            num_kv_heads=num_kv_heads,
            dropout=dropout,
        )
        self.norm1 = RMSNorm(embed_dim)
        self.norm2 = RMSNorm(embed_dim)
        self.ff = SwiGLUFeedForward(embed_dim, dropout=dropout)

    def forward(self, x, layer_past=None, use_cache=False, start_pos=0):
        attn_out, present = self.attention(
            self.norm1(x),
            layer_past=layer_past,
            use_cache=use_cache,
            start_pos=start_pos,
        )
        x = x + attn_out
        x = x + self.ff(self.norm2(x))
        return x, present


class SusaGPT(nn.Module):
    def __init__(
        self,
        vocab_size,
        embed_dim=64,
        num_heads=4,
        num_kv_heads=2,
        num_layers=2,
        max_len=512,
        dropout=0.1,
    ):
        super().__init__()

        self.vocab_size = vocab_size
        self.embed_dim = embed_dim
        self.num_heads = num_heads
        self.num_kv_heads = num_kv_heads
        self.num_layers = num_layers
        self.max_len = max_len
        self.dropout = dropout

        self.embedding = EmbeddingLayer(vocab_size, embed_dim)
        self.embedding_dropout = nn.Dropout(dropout)
        self.blocks = nn.ModuleList(
            [
                TransformerBlock(
                    embed_dim=embed_dim,
                    num_heads=num_heads,
                    num_kv_heads=num_kv_heads,
                    dropout=dropout,
                )
                for _ in range(num_layers)
            ]
        )
        self.norm = RMSNorm(embed_dim)

        self.output = nn.Linear(embed_dim, vocab_size, bias=False)
        self.output.weight = self.embedding.embedding.weight

    def forward(self, x, kv_cache=None, use_cache=False, start_pos=0):
        x = self.embedding(x)
        x = self.embedding_dropout(x)

        next_cache = [] if use_cache else None

        for layer_index, block in enumerate(self.blocks):
            layer_past = None if kv_cache is None else kv_cache[layer_index]
            x, present = block(
                x,
                layer_past=layer_past,
                use_cache=use_cache,
                start_pos=start_pos,
            )
            if use_cache:
                next_cache.append(present)

        x = self.norm(x)
        logits = self.output(x)

        if use_cache:
            return logits, next_cache
        return logits


TinyGPT = SusaGPT


if __name__ == "__main__":
    model = SusaGPT(
        vocab_size=768,
        embed_dim=64,
        num_heads=4,
        num_kv_heads=2,
        num_layers=2,
        max_len=32,
        dropout=0.1,
    )
    sample_input = torch.tensor([[1, 2, 3, 4, 5]])
    output = model(sample_input)
    print("Model ready!")
    print(f"Output shape : {output.shape}")
