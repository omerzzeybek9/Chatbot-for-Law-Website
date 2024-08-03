import re
from datasets import load_dataset
import json

def clean_text(text):
    text = text.replace('&nbsp;', ' ')
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    return text

def clean_dataset(dataset):
    def clean_example(example):
        example['text'] = [clean_text(t) for t in example['text']]
        return example

    return dataset.map(clean_example)

dataset = load_dataset("json", data_files="data.jsonl", split="train")

cleaned_dataset = clean_dataset(dataset)

def save_to_jsonl(dataset, file_path):
    with open(file_path, 'w', encoding="utf-8") as f:
        for example in dataset:
            f.write(json.dumps(example, ensure_ascii=False) + '\n')

save_to_jsonl(cleaned_dataset, "cleaned_dataset.jsonl")
