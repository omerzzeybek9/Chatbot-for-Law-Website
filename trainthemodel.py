import json
from datasets import load_dataset
from transformers import AutoTokenizer, DataCollatorWithPadding
import torch
from transformers import AutoModelForSequenceClassification, Trainer, TrainingArguments

#Load dataset
dataset = load_dataset("json", data_files="cleaned_dataset.jsonl", split="train")

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

def tokenize(example):
    text = ' '.join(example['text'])
    return tokenizer(text, truncation=True, padding='max_length', max_length=512)

tokenized_dataset = dataset.map(tokenize, batched=False)

data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

print(tokenized_dataset)

train_size = 0.8
train_dataset = tokenized_dataset.shuffle(seed=42).select(range(int(len(tokenized_dataset) * train_size)))
eval_dataset = tokenized_dataset.shuffle(seed=42).select(range(int(len(tokenized_dataset) * train_size), len(tokenized_dataset)))

model = AutoModelForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=2)

training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=3,
    weight_decay=0.01,
)


trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    tokenizer=tokenizer,
    data_collator=data_collator,
)


trainer.train()


model.save_pretrained("saved_model")
tokenizer.save_pretrained("saved_tokenizer")