# Filename: HuggingFace_Guide.md

# Hugging Face: AI ka Home (Complete Guide)

Hugging Face (HF) AI models, datasets aur applications ke liye "GitHub of AI" hai. Aaj ke time pe models use karne ke liye ye repository sabse badi hai.

## 1. Hugging Face kya hai?
HF 3 main pieces mein split hai:
- **Hub:** Jahan models, datasets aur Spaces (demos) hosted hain.
- **Transformers Library:** Pre-trained models ko load aur run karne ke liye.
- **Datasets Library:** High-quality text, image, audio data ke liye.

## 2. Transformers `pipeline()` — Sabse Aasan Way
Agar aapko text classification, translation ya summarization ke liye direct model chahiye, toh pipeline use karo. Isme model loading handle ho jaati hai backend mein.

```python
from transformers import pipeline

# Sentiment Analysis logic
classifier = pipeline("sentiment-analysis")
res = classifier("I love building AI tools!")
print(f"Sentiment: {res}")

# Summarizer pipeline
summarizer = pipeline("summarization")
# article = "..." 
# summary = summarizer(article, max_length=50)
```

## 3. AutoModel aur AutoTokenizer — Manual Control
Real usage mein humein tokenizer aur model class optimize karke load karni hoti hai.

```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification

model_id = "bert-base-uncased" # Kisi bhi model ka ID HF Hub se
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForSequenceClassification.from_pretrained(model_id)

# Model ka actual input preparation
inputs = tokenizer("Hello HF!", return_tensors="pt")
outputs = model(**inputs)
```

## 4. Datasets Library — ML ke liye Fuel
`datasets` library bade large scale datasets download aur manipulate karne ke liye bani hai.

```python
from datasets import load_dataset

# Dataset load karna (IMDb dataset ek popular text dataset hai)
ds = load_dataset("imdb")

# Operations: Map (har entry pe transformation), Filter, Train-Test split
ds_tokenized = ds.map(lambda x: tokenizer(x["text"], truncation=True), batched=True)
train_test = ds["train"].train_test_split(test_size=0.1)
```

## 5. Model Hub — Apna Model Upload karna
Aapne naya model train kiya? use upload kar sakte hain HF CLI ya Hub API se. Model Card (`README.md`) zaroori hai specify karne ke liye model kya karta hai.

```bash
# Terminal command model upload ke liye
# huggingface-cli login
# huggingface-cli upload my-awesome-model .
```

## 6. Inference API (Free & Paid)
Bina model download kiye, HTTP request (Curl) karke results mangwana. Ye web applications ke liye best hai.

```python
import requests

API_URL = "https://api-inference.huggingface.co/models/gpt2"
headers = {"Authorization": "Bearer YOUR_HF_TOKEN"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()

# output = query({"inputs": "Once upon a time..."})
```

## 7. Spaces — Gradio se Deploy
Hugging Face Spaces par aap apna AI demo file kar sakte hain bina server manage kiye.

```python
import gradio as gr

def greet(name):
    return "Hello " + name + "!!"

iface = gr.Interface(fn=greet, inputs="text", outputs="text")
# iface.launch() # Is script ko HF Spaces pe 'app.py' banakar upload karein.
```

## 8. Common Errors aur Solutions
- **CUDA Out of Memory:** Batch size kam karein ya `model.half()` (FP16) use karein.
- **Tokenizer mismatch:** Model load karne ke waqt sahi `model_id` ensure karein.
- **Gateway Timeout:** Inference API limit se zyada calls ho rahi hain.
- **Token expired:** Apna local login environment dobara check karein.
