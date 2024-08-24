import json


with open('cleaned_dataset.jsonl', 'r', encoding="utf-8") as infile, open('output.jsonl', 'w', encoding="utf-8") as outfile:
    for line in infile:
        data = json.loads(line)
        url = data["url"]
        texts = " ".join(data["text"])
        prompt_completion = {"prompt": texts, "completion": url}
        outfile.write(json.dumps(prompt_completion, ensure_ascii=False) + '\n')