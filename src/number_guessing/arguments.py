import argparse
import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()
# Read model name from environment variable
model_name = os.getenv("MODEL_NAME")
if not model_name:
    raise ValueError("❌ Environment variable MODEL_NAME is not set.")

argparser = argparse.ArgumentParser()

argparser.add_argument("--model_version", type=str, default=model_name)
argparser.add_argument("--persona", type=str, default='default')

argparser.add_argument("--set_guess_number", dest='set_guess_number', action='store_true')
argparser.set_defaults(set_guess_number=False)

argparser.add_argument("--interpretation_guess", dest='interpretation_guess', action='store_true')
argparser.set_defaults(interpretation_guess=False)
argparser.add_argument("--advanced", type=str, default='default')
