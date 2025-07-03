import os
from openai import OpenAI
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()
# Read model name from environment variable
model_name = os.getenv("MODEL_NAME")
if not model_name:
    raise ValueError("❌ Environment variable MODEL_NAME is not set.")

client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="EMPTY"  # Not needed for local vLLM, but required by SDK
)

response = client.chat.completions.create(
    model=model_name,
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is the capital of France?"}
    ],
    temperature=0.7,
    max_tokens=100
)

print("Assistant:", response.choices[0].message.content.strip())
