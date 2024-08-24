import json

input_file = 'output.jsonl'
output_file = 'chat_format.jsonl'

with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
    for line in infile:
        data = json.loads(line)
        prompt = data.get("prompt")
        completion = data.get("completion")
        completion = completion.replace("https://bilginhukuk.av.tr/","").replace("/","")
        completion = " ".join(completion.split("-"))
        completion = completion.title()

        if prompt and completion:
            chat_format = { "messages" :
                    [{"role" : "system", "content" : "This chatbot is trained to answer law-related questions correctly. It should give the most accurate answer based on the given article title and content."},
                    {"role" : "user", "content" : completion + " ile ilgili makale soruları"},
                    {"role" : "assistant", "content" : prompt}]
            }
            outfile.write(json.dumps(chat_format,ensure_ascii=False) + '\n')