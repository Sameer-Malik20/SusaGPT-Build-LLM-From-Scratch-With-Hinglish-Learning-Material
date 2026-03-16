from functools import lru_cache
from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel, Field

from config import API_CONFIG
from generate import generate, load_everything


# api.py project ko REST API ke form me expose karta hai.
# Ye portfolio aur real-world integration dono ke liye useful hota hai.
# FastAPI ka fayda:
# 1. simple syntax
# 2. automatic docs
# 3. JSON request/response support


app = FastAPI(
    title="MyLLM API",
    description="SusaGPT style local language model API",
    version="1.0.0",
)


class GenerateRequest(BaseModel):
    prompt: str = Field(..., description="User ka input prompt")
    max_new_tokens: int | None = Field(default=None, ge=1, le=256)
    temperature: float | None = Field(default=None, gt=0.0, le=3.0)
    top_k: int | None = Field(default=None, ge=0)
    top_p: float | None = Field(default=None, gt=0.0, le=1.0)
    repetition_penalty: float | None = Field(default=None, ge=1.0, le=2.0)
    use_kv_cache: bool | None = None
    use_beam_search: bool = False
    beam_width: int | None = Field(default=None, ge=1, le=8)
    sampling_mode: Literal["topk_topp", "mirostat"] = "topk_topp"
    mirostat_tau: float | None = Field(default=None, gt=0.0, le=10.0)
    mirostat_eta: float | None = Field(default=None, gt=0.0, le=2.0)
    prefer_quantized: bool = True


@lru_cache(maxsize=2)
def get_runtime(prefer_quantized: bool):
    # Runtime ko cache kar rahe hain taaki har request par model dubara load na ho.
    model, tokenizer, model_path = load_everything(
        prefer_quantized=prefer_quantized,
        return_path=True,
    )
    return model, tokenizer, str(model_path)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "host": API_CONFIG["host"],
        "port": API_CONFIG["port"],
    }


@app.get("/model-info")
def model_info(prefer_quantized: bool = True):
    model, tokenizer, model_path = get_runtime(prefer_quantized)
    return {
        "model_path": model_path,
        "vocab_size": tokenizer.vocab_size,
        "embed_dim": model.embed_dim,
        "num_heads": model.num_heads,
        "num_kv_heads": model.num_kv_heads,
        "num_layers": model.num_layers,
        "max_len": model.max_len,
        "dropout": model.dropout,
    }


@app.post("/generate")
def generate_text(request: GenerateRequest):
    model, tokenizer, model_path = get_runtime(request.prefer_quantized)

    text = generate(
        model=model,
        tokenizer=tokenizer,
        prompt=request.prompt,
        max_new_tokens=request.max_new_tokens,
        temperature=request.temperature,
        top_k=request.top_k,
        top_p=request.top_p,
        repetition_penalty=request.repetition_penalty,
        use_kv_cache=request.use_kv_cache,
        use_beam_search=request.use_beam_search,
        beam_width=request.beam_width,
        sampling_mode=request.sampling_mode,
        mirostat_tau=request.mirostat_tau,
        mirostat_eta=request.mirostat_eta,
    )

    return {
        "prompt": request.prompt,
        "response": text,
        "sampling_mode": request.sampling_mode,
        "use_beam_search": request.use_beam_search,
        "model_path": model_path,
        "quantized": request.prefer_quantized,
    }


if __name__ == "__main__":
    # Run command:
    # uvicorn api:app --host 127.0.0.1 --port 8000 --reload
    print("FastAPI app ready.")
    print(f"Run with: uvicorn api:app --host {API_CONFIG['host']} --port {API_CONFIG['port']} --reload")
