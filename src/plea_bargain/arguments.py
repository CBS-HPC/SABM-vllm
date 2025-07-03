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


argparser.add_argument('--gui', dest='gui', action='store_true')
argparser.set_defaults(gui=False)

argparser.add_argument("--model_version", type=str, default=model_name)
argparser.add_argument("--tcu_test", dest='tcu_test', action='store_true')
argparser.set_defaults(tcu_test=False)
argparser.add_argument("--persona", type=str, default='persona')
argparser.add_argument("--no_fewshot", dest='no_fewshot', action='store_false')
argparser.set_defaults(no_fewshot=True)
argparser.add_argument("--output_max_tokens", type=int, default=64)

argparser.add_argument("--num_agents", type=int, default=100)
argparser.add_argument("--task", type=str, default='1')
