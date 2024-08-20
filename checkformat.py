import json
from collections import defaultdict

with open("output.jsonl", "r", encoding="utf-8") as f:
    dataset = [json.loads(line) for line in f]

print("Num examples:", len(dataset))
print("First example:")
print(dataset[0])

format_errors = defaultdict(int)

for ex in dataset:
    if not isinstance(ex, dict):
        format_errors["data_type"] += 1
        continue

    prompt = ex.get("prompt", None)
    completion = ex.get("completion", None)
    
    if not prompt or not isinstance(prompt, str):
        format_errors["missing_or_invalid_prompt"] += 1

    if not completion or not isinstance(completion, str):
        format_errors["missing_or_invalid_completion"] += 1

if format_errors:
    print("Found errors:")
    for k, v in format_errors.items():
        print(f"{k}: {v}")
else:
    print("No errors found")