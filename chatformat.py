import json

input_file = 'output.jsonl'
output_file = 'chat_format.jsonl'

with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
    for line in infile:
        data = json.loads(line)
        prompt = data.get("prompt")
        completion = data.get("completion")

        if prompt and completion:
            chat_format = {
                "messages": [
                    {"role": "user", "content": prompt},
                    {"role": "assistant", "content": completion}
                ]
            }
            outfile.write(json.dumps(chat_format,ensure_ascii=False) + '\n')