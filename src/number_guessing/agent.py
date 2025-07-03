import time
import os
from dotenv import load_dotenv
from openai import OpenAI
from openai._exceptions import RateLimitError, APIStatusError, OpenAIError


class Agent:
    def __init__(self, temperature=1.0, model=None, max_tokens=200, api_key = ''):
        
        if not model:
            # Load variables from .env file
            load_dotenv()
            # Read model name from environment variable
            model = os.getenv("MODEL_NAME")
            if not model:
                raise ValueError("❌ Environment variable MODEL_NAME is not set.")

        
        self.temperature = temperature
        self.model = model
        self.max_tokens = max_tokens

    
    def communicate(self, context):
        prompt = context + "\n\n"
        message = ""

        retries = 3
        backoff_factor = 2
        current_retry = 0

        client = OpenAI(base_url="http://localhost:8000/v1", api_key="EMPTY")

        while current_retry < retries:
            try:
                response = client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "user", "content": prompt},
                        {"role": "user", "content": ""}
                    ],
                    max_tokens=self.max_tokens,
                    temperature=self.temperature,
                    top_p=1
                )
                message = response.choices[0].message.content.strip().lower()
                return message
            except RateLimitError as e:
                if current_retry < retries - 1:
                    wait_time = backoff_factor ** current_retry
                    print(f"RateLimitError: Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                    current_retry += 1
                else:
                    print(f"Error {e}")
                    raise e
            except OpenAIError as e:
                if current_retry < retries - 1:
                    wait_time = backoff_factor ** current_retry
                    print(f"RateLimitError: Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                    current_retry += 1
                else:
                    raise e
            except Exception as e:
                if current_retry < retries - 1:
                    wait_time = backoff_factor ** current_retry
                    print(f"RateLimitError: Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                    current_retry += 1
                else:
                    print(f"Error {e}")
                    raise e
