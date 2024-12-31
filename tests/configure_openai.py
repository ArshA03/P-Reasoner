from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv("env/.env")


client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=os.getenv("API_KEY"),
)

completion = client.chat.completions.create(
  model="openai/gpt-3.5-turbo",
  messages=[
    {
      "role": "user",
      "content": "What is the meaning of life?"
    }
  ]
)
print(completion.choices[0].message.content)