from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

#Load model and tokenizer
model_path = "./trained_model"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path)

#Create Text Generation pipeline
generator = pipeline('text-generation', model=model, tokenizer=tokenizer)

#Chatbot
def chat_with_bot(prompt):
    prompt = (
        "Sen bir hukuk websitesinin yapay zeka asistanısın. Sana öğrettiğim verilerle sorulara hukuki bir şekilde cevap ver. "
        "Eğer yardım istenirse veya iletişim bilgisi istenirse iletişim bilgilerini ver.\n"
        f"Kullanıcı: {user_input}\nYanıt:")

    response = generator(prompt, max_length=300, num_return_sequences=1, temperature=0.7, top_k=50, top_p=0.95)
    generated_text = response[0]['generated_text']

    answer = generated_text.replace(prompt, '').strip()
    return answer


#Take input and answer
while True:
    user_input = input("Soru: ")
    if user_input.lower() in ["exit", "quit", "q"]:
        break
    response = chat_with_bot(user_input)
    print(f"Cevap: {response}")