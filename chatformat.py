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
                    [{"role" : "system", "content" : "Bilgin AI is a chatbot for Bilgin Hukuk website. He talks turkish and answers questions from assistants prompt part and gives contact details in every conversation"}, 
                    {"role" : "user", "content" : completion}, 
                    {"role" : "assistant", "content" : prompt}]
            }
            outfile.write(json.dumps(chat_format,ensure_ascii=False) + '\n')