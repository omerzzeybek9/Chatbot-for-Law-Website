import openai

openai.api_key = "api"

response = openai.files.create(
    file = open("formatted_data.jsonl", "rb"),
    purpose = "fine-tune"
)

file_id = response.id


fine_tune = openai.fine_tuning.jobs.create(
  training_file=file_id, 
  model="gpt-3.5-turbo"
)




