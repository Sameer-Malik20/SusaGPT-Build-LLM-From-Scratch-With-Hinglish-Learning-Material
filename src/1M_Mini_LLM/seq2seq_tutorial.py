from transformers import (
    T5Tokenizer,
    T5ForConditionalGeneration,
    Trainer,
    TrainingArguments
)

from datasets import Dataset

# --------------------------
# Dataset
# --------------------------

data = [
    {
        "input": "translate: hello",
        "target": "namaste"
    },
    {
        "input": "translate: how are you",
        "target": "kaise ho"
    },
    {
        "input": "translate: i love cricket",
        "target": "mujhe cricket pasand hai"
    },
    {
        "input": "summarize: Sameer is a student. Sameer loves cricket. Sameer studies AI.",
        "target": "Sameer studies AI and loves cricket."
    },
    {
        "input": "correct: I are good",
        "target": "I am good"
    },
    {
        "input": "paraphrase: He is very smart",
        "target": "He is extremely intelligent"
    }
]

dataset = Dataset.from_list(data)

# --------------------------
# Model
# --------------------------

tokenizer = T5Tokenizer.from_pretrained("t5-small")

model = T5ForConditionalGeneration.from_pretrained(
    "t5-small"
)

# --------------------------
# Tokenization
# --------------------------

def preprocess(example):

    inputs = tokenizer(
        example["input"],
        max_length=64,
        truncation=True,
        padding="max_length"
    )

    targets = tokenizer(
        example["target"],
        max_length=64,
        truncation=True,
        padding="max_length"
    )

    inputs["labels"] = targets["input_ids"]

    return inputs


tokenized_dataset = dataset.map(preprocess)

# --------------------------
# Training
# --------------------------

training_args = TrainingArguments(
    output_dir="./seq2seq_demo",
    per_device_train_batch_size=2,
    num_train_epochs=50,
    logging_steps=1,
    save_strategy="no"
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset
)

trainer.train()

# --------------------------
# Testing
# --------------------------

def generate(text):

    inputs = tokenizer(
        text,
        return_tensors="pt"
    )

    outputs = model.generate(
        **inputs,
        max_new_tokens=30
    )

    print(
        tokenizer.decode(
            outputs[0],
            skip_special_tokens=True
        )
    )


generate("translate: hello")
generate("translate: how are you")
generate("summarize: Sameer is a student. Sameer loves cricket. Sameer studies AI.")
generate("correct: I are good")
generate("paraphrase: He is very smart")