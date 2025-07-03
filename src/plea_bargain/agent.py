from openai import OpenAI
import os
from dotenv import load_dotenv
from openai._exceptions import RateLimitError, APIStatusError, OpenAIError
import time

class PersonalizedAgent:
    def __init__(self, id, gender, ethnicity, education, occupation, location, temperature=0.8, model=None, max_tokens=64, persona = "", api_key = ""):
        
        if not model:
            # Load variables from .env file
            load_dotenv()
            # Read model name from environment variable
            model = os.getenv("MODEL_NAME")
            if not model:
                raise ValueError("❌ Environment variable MODEL_NAME is not set.")

        self.id = id
        self.gender = gender
        self.ethnicity = ethnicity
        self.education = education
        self.occupation = occupation
        self.location = location
        self.personality_score = 0
        self.temperature = temperature
        self.persona = persona
        self.tcu_scale = None

        self.group = 1
        self.decision = {}
        self.decision_reason = {}

        self.model = model
        self.max_tokens = max_tokens

        self.api_key = api_key
    
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
                #print(message)
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
            except Exception as e:
                if current_retry < retries - 1:
                    wait_time = backoff_factor ** current_retry
                    print(f"RateLimitError: Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                    current_retry += 1
                else:
                    print(f"Error {e}")
                    raise e

    def generate_persona(self):
        persona = f"{self.gender}, {self.ethnicity}, {self.education}, {self.occupation}, living in a {self.location} area"
        return persona
