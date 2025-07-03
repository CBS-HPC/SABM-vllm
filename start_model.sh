#!/bin/bash

# ----------------------------------------
# LOAD ENVIRONMENT VARIABLES
# ----------------------------------------

if [ -f ".env" ]; then
  echo "Loading environment variables from .env..."
  set -o allexport
  source .env
  set +o allexport
else
  echo "❌ .env file not found. Please create one with HF_TOKEN set."
  exit 1
fi

# Check if HF_TOKEN is set
if [ -z "$HF_TOKEN" ]; then
  echo "❌ HF_TOKEN is not set in your .env file."
  exit 1
fi

# ----------------------------------------
# MODEL REGISTRY AND CONFIG
# ----------------------------------------

declare -A MODEL_REGISTRY=(
  ["llama3-70b"]="meta-llama/Meta-Llama-3-70B-Instruct"
  ["llama3-8b"]="meta-llama/Meta-Llama-3-8B-Instruct"
  ["mixtral"]="mistralai/Mixtral-8x7B-Instruct-v0.1"
  ["command-r"]="CohereForAI/c4ai-command-r-plus"
  ["qwen2"]="Qwen/Qwen2-72B-Instruct"
)

declare -A TP_SIZES=(
  ["llama3-70b"]=4
  ["llama3-8b"]=1
  ["mixtral"]=2
  ["command-r"]=1
  ["qwen2"]=4
)

# Parse model key from first argument
MODEL_KEY=$1

if [ -z "$MODEL_KEY" ] || [ -z "${MODEL_REGISTRY[$MODEL_KEY]}" ]; then
  echo "❌ Invalid or missing model key."
  echo "Usage: $0 <model-key>"
  echo "Available models:"
  for key in "${!MODEL_REGISTRY[@]}"; do
    echo "  - $key"
  done
  exit 1
fi

MODEL_NAME="${MODEL_REGISTRY[$MODEL_KEY]}"
TP_SIZE="${TP_SIZES[$MODEL_KEY]}"
MODEL_CACHE_DIR="./.cache/models/$MODEL_KEY"
PORT=8000

# ----------------------------------------
# UPDATE .env WITH SELECTED MODEL
# ----------------------------------------

# Ensure .env ends with a newline
tail -c1 .env | read -r _ || echo >> .env

if grep -q "^MODEL_NAME=" .env; then
  sed -i.bak "s|^MODEL_NAME=.*|MODEL_NAME=${MODEL_NAME}|" .env
else
  echo "MODEL_NAME=${MODEL_NAME}" >> .env
fi

echo "✅ MODEL_NAME saved to .env as: $MODEL_NAME"

# ----------------------------------------
# ACTIVATE VENV (IF EXISTS)
# ----------------------------------------

if [ -d ".venv" ]; then
  echo "Activating virtual environment (.venv)..."
  source .venv/bin/activate
else
  echo "⚠️ No .venv directory found. Proceeding without activating a virtual environment."
fi

# ----------------------------------------
# CHECK GPU AVAILABILITY
# ----------------------------------------

available_gpus=$(nvidia-smi --query-gpu=index --format=csv,noheader | wc -l)

echo "Detected $available_gpus GPU(s) available."

if [ "$available_gpus" -lt "$TP_SIZE" ]; then
  echo "❌ Not enough GPUs available. Required: $TP_SIZE, Available: $available_gpus"
  exit 1
fi

# ----------------------------------------
# PREPARE CACHE DIRECTORY
# ----------------------------------------

mkdir -p "$MODEL_CACHE_DIR"

# ----------------------------------------
# START SERVER
# ----------------------------------------

echo "Starting vLLM server for model: $MODEL_NAME"
python3 -m vllm.entrypoints.openai.api_server \
  --model "$MODEL_NAME" \
  --port "$PORT" \
  --tensor-parallel-size "$TP_SIZE" \
  --download-dir "$MODEL_CACHE_DIR"
echo "Server is Ready!"