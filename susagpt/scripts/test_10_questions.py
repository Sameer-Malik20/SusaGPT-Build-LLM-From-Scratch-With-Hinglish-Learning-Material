import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from susagpt.src.generate import load_everything, generate_hybrid
from susagpt.src.config import BASE_MODEL_PATH

model, tokenizer = load_everything(model_path=BASE_MODEL_PATH, prefer_quantized=False)

questions = [
    "what is the role of ai in susalabs healthcare projects",
    "how does susalabs help startups scale",
    "does susalabs build custom backend systems",
    "explain how ai-powered crm can drive business growth",
    "is susalabs a global it company",
    "what technologies does susalabs support for healthcare research",
    "does susalabs offer predictive analytics solutions",
    "why should a business choose custom software over off the shelf solutions",
    "can we integrate erp systems with susalabs mobile apps",
    "how can we contact susalabs to build the future"
]

print("=" * 80)
print("SusaGPT — 10 Custom Complex/Short Questions Evaluation")
print("=" * 80)

for idx, q in enumerate(questions, 1):
    print(f"\n[Q{idx}] {q}")
    ans = generate_hybrid(q, model, tokenizer)
    print(f"Answer: {ans}")

print("=" * 80)
