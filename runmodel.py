from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("./results")
model = AutoModelForCausalLM.from_pretrained("./results")

# Örnek input
input_text = "Yapı kayıt belgesinin iptali davalarında anayasaya aykırılık iddiası nedir?"

# Tokenize input
inputs = tokenizer(input_text, return_tensors="pt")

# Modeli çalıştır ve output al
outputs = model.generate(**inputs, max_length=512, num_return_sequences=1)

# Outputu çöz
response = tokenizer.decode(outputs[0], skip_special_tokens=True)

print(response)