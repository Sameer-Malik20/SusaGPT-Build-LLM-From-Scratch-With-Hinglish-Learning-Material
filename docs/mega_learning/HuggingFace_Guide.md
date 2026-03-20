# 🤗 Hugging Face: AI Ecosystem (Expert Guide)
> **Level:** Beginner → Expert | **Language:** Hinglish | **Goal:** Master transformers, datasets, Spaces, and HF inference

---

## 📋 Is Guide Se Kya Seekhoge

| Section | Topic | Why? |
|---------|-------|------|
| 1. HF Hub Mastery | Model Tags, Datasets, Versions | Navigating the Hub |
| 2. Transformers Deep Dive | AutoModel, Configuration, Tokenizer | Model internals |
| 3. Datasets Library | Mapping, Streaming, Sharding | Large-scale data |
| 4. Trainer API | Custom Loss & Evaluation | Fine-tuning models |
| 5. Inference & Production | Inference API, vLLM on HF | Real-world usage |
| 6. Gradio & Spaces | Demos and Deployment | Showcasing work |

---

## 1. 📂 Hugging Face Hub: The Central OS of AI

Hugging Face sirf models nahi, ek poora **Infrastructure** hai. Aaj Llama, BERT, Stable Diffusion sab isi se operate hote hain.

- **Model Hub:** Jahan weights (bin/safetensors) aur model cards (README) hote hain.
- **Dataset Hub:** Text (Parquet/JSON), Audio, Image collection.
- **Spaces:** AI apps run karne ka platform.

---

## 2. 🏗️ Transformers Internals: Master the Base

Transformers library do main inputs use karti hai: **Tokenizer** (Text -> Numbers) aur **Model** (Numbers -> Understanding).

### A. AutoClasses — The AI Magic
Hamein BERT ya GPT class yaad rakhne ki zaroorat nahi. `Auto` classes apne aap model shape detect kar leti hain.

```python
from transformers import AutoTokenizer, AutoModelForCausalLM

model_id = "gpt2" # Example model
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id)

# Tokenizer details
text = "Transformers are amazing!"
tokens = tokenizer(text, return_tensors="pt")
print(tokens["input_ids"]) # Numerical IDs
# Output: tensor([[...]])
```

### B. Bit Quantization (BitsAndBytes)
Large models ko kam memory mein chalane ke liye 4-bit ya 8-bit use hota hai.

```python
# !pip install bitsandbytes
# model = AutoModelForCausalLM.from_pretrained(model_id, load_in_4bit=True)
```

---

## 3. 📊 Datasets Library: Handling Big Data

Bade datasets memory mein fit nahi hote. Iske liye hum **Streaming mode** use karte hain.

```python
from datasets import load_dataset

# Streaming mode: Data fetch on-the-fly (No download)
ds = load_dataset("wikipedia", date="20220301", language="en", streaming=True)

# Dataset processing
train_ds = ds["train"].shuffle(seed=42).take(100)
for example in train_ds:
    print(example["text"]) # Read one by one
```

**Common Op:** Dataset Clean-up
```python
# Filter and Map
# filtered_ds = ds.filter(lambda x: len(x['text']) > 100)
# tokenized_ds = ds.map(lambda x: tokenizer(x['text']), batched=True)
```

---

## 4. 🚀 Trainer API: Customize Training Loops

Manual training loop (PyTorch) thoda complex ho sakta hai. HF Trainer optimization manage karta hai (distributed training, mixed precision).

```python
from transformers import Trainer, TrainingArguments

# Training Config
training_args = TrainingArguments(
    output_dir="./results",
    per_device_train_batch_size=8,
    num_train_epochs=3,
    logging_dir='./logs',
    fp16=True # Mixed precision speed-up
)

# Trainer logic (Simulated)
# trainer = Trainer(
#     model=model,
#     args=training_args,
#     train_dataset=tokenized_ds,
#     eval_dataset=eval_ds
# )
# trainer.train()
```

---

## 5. ⚡ Inference & Real Production: Hub to Web

Model weights load karke web endpoints banana via **Inference API**.

```python
import requests

HF_TOKEN = "your_hf_token_here"
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-v0.1"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

# response = query({"inputs": "Explain AI in three sentences."})
```

---

## 🏗️ Mega Project: AI Image Generator with Gradio on HF Spaces

Is project mein hum ek Stable Diffusion model host karenge ek interactive UI (`Gradio`) ke saath.

```python
import gradio as gr
from diffusers import StableDiffusionPipeline
import torch

# 1. Load Model logic
pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
if torch.cuda.is_available(): pipe.to("cuda")

# 2. Function logic
def generate_img(prompt):
    return pipe(prompt).images[0]

# 3. UI logic
# interface = gr.Interface(fn=generate_img, inputs="text", outputs="image")
# interface.launch()
```

---

## 🧪 Quick Test — Expert Level Check!

### Q1: Safetensors logic
`.bin` file aur `.safetensors` file mein kya fark hai?
<details><summary>Answer</summary>
`.bin` files (pickle based) unsafe ho sakte hain code execution ke liye. `.safetensors` **secure**, **fast loading**, aur memory-mapping support karte hain.
</details>

### Q2: Tokenization logic
Agar naya model (Llama) load karne par "Tokenizer file not found" error aaye, toh fix kya hai?
<details><summary>Answer</summary>
1. Check model repo on Hub (tokenizer.json hai ya nahi).
2. `use_fast=True` parameter hatakar ya lagakar check karein.
3. Hugging Face login check karein (Gated models ke liye token chahiye).
</details>

---

## 🔗 Resources
- [HF Course (Official)](https://huggingface.co/learn/nlp-course)
- [Transformer Models Roadmap](https://huggingface.co/models)
- [Gradio Documentation](https://gradio.app/docs/)
