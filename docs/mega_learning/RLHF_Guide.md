# Filename: RLHF_Guide.md

# RLHF (Reinforcement Learning from Human Feedback): Complete Guide

LLMs ko helpful, harmless, aur honest banane ke liye RLHF sabse mukhya (core) technique hai. Isse ChatGPT jaise models ko unke outputs sudharne mein madad milti hai.

## 1. RLHF kya hai?
Normal superivsed training (SFT) se model sirf texts repeat karna seekhta hai. RLHF se model seekhta hai ki "Insano ko kaunsa answer zyada pasand hai". 
Iska matlab model ke answers ko ranks di jaati hain, aur model un ranks (feedback) se seekhta hai.

## 2. Pura Workflow: 3 Stages
RLHF basically 3 parts mein divided hai:
1. **SFT (Supervised Fine Tuning):** Prompt aur complete (good) answers ke pair par model train karna.
2. **Reward Model (RM) Training:** Model se 2 ya zyada answers generate karwana, aur insano se best choose karwana (preference pairs).
3. **PPO (Proximal Policy Optimization):** Reward model ka score use karke RL (Reinforcement Learning) loop chalana model ko behtar banane ke liye.

## 3. Preference Data: Model ka Teacher
Jab ek prompt ke liye 2 options hon:
- **A:** "Aapka din kaisa hai?"
- **B:** "Main ek AI model hoon."
Agar humans **A** ko prefer karte hain, toh ye pair ban jaata hai: `(Prompt, preferred_response, rejected_response)`.

## 4. Reward Model: Scorer
Reward Model model ka hi ek version hota hai jo text input lekar ek number (score) deta hai.

```python
# Pseudo-logic check for RM
# prompt = "Recipe for pasta?"
# response_1 = "..." (Great) -> Score: 0.8
# response_2 = "..." (Bad) -> Score: 0.1
```

## 5. PPO (Reinforcement Learning)
PPO model ko allow karta hai "Seekhne" ki (adjust weights) reward badhane ke liye, bina pichla knowledge poora kharab kiye (clipping logic). 
Insan agar Model ko "acha" bolenge, toh Reward Model score badhayega, aur PPO optimize kareka model ko same direction mein.

## 6. DPO (Direct Preference Optimization) — Modern Alternative
RLHF bahut slow aur unstable hota hai. DPO ne ise simpler bana diya. Isme koi separate "Reward Model" nahi chahiye hota. Ye seedha mathematical comparison se model ko optimize kar deta hai. 

## 7. Mini Project: TRL library se DPO Pipeline
`trl` library (Transformer Reinforcement Learning) Hugging Face ne RLHF aur DPO ke liye banayi hai.

```python
from trl import DPOConfig, DPOTrainer
from transformers import AutoModelForCausalLM, AutoTokenizer
from datasets import load_dataset

model_id = "gpt2" # simple base model target
model = AutoModelForCausalLM.from_pretrained(model_id)
tokenizer = AutoTokenizer.from_pretrained(model_id)

# Dataset format (Prompts + Chosen + Rejected)
# dataset = load_dataset("json", data_files="preference_data.json")

# Config and Training
# training_args = DPOConfig(output_dir="./dpo_model", beta=0.1)
# trainer = DPOTrainer(model, args=training_args, train_dataset=dataset, tokenizer=tokenizer)
# trainer.train()
```
