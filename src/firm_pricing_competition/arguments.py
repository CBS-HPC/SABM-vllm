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
argparser.add_argument("--rounds", type=int, default=1000)
argparser.add_argument("--output_max_tokens", type=int, default=128)
argparser.add_argument("--breakpoint_rounds", type=int, default=20)
argparser.add_argument("--persona_firm1", type=int, default=1)
argparser.add_argument("--persona_firm2", type=int, default=1)
argparser.add_argument("--set_initial_price", dest='set_initial_price', action='store_true')
argparser.set_defaults(set_initial_price=False)

argparser.add_argument("--cost", type=int, default=[2,2], nargs=2)
argparser.add_argument("--parameter_a", type=float, default=14)
argparser.add_argument("--parameter_d", type=float, default=0.00333333333333)
argparser.add_argument("--parameter_beta", type=float, default=0.00666666666666)
argparser.add_argument("--initial_price", type=int, default=[2,2], nargs=2)
argparser.add_argument("--load_data_location", type=str, default='')

argparser.add_argument('--strategy', dest='strategy', action='store_true')
argparser.set_defaults(strategy=True)
argparser.add_argument('--has_conversation', dest='has_conversation', action='store_true')
argparser.set_defaults(has_conversation=False)
