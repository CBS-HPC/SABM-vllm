# Smart Agent-Based Modeling (SABM)

This is an **adapted version** of the official codebase from the paper:  
**[Smart Agent-Based Modeling: On the Use of Large Language Models in Computer Simulations](https://arxiv.org/abs/2311.06330)**  
*Zengqing Wu, Run Peng, Xu Han, Shuyuan Zheng, Yixin Zhang, Chuan Xiao. 2023.*

> ✅ This version has been adapted to run **locally** using **Hugging Face models** via [`vLLM`](https://github.com/vllm-project/vllm), instead of the OpenAI API.

This repository is a **fork of** [Roihn/SABM](https://github.com/Roihn/SABM), modified to support local inference using Hugging Face models through `vLLM`.  
It removes the dependency on OpenAI's GPT-4 API and enables reproducible experiments on your own hardware using open-access LLMs.

## Setup

### Clone the Repository

```bash
git clone https://github.com/CBS-HPC/SABM-vllm.git
cd SABM-vllm
```

### Create Python Environment (using `uv`)

We recommend using [`uv`](https://github.com/astral-sh/uv) for fast dependency management and isolated virtual environments.

If you don't have `uv` installed, you can install it with:

```bash
pip install uv
```

Initialize a new `uv` project, create a virtual environment, and install the dependencies listed in `requirements.txt`:

```bash
uv init
uv venv
uv add -r requirements.txt
```

This will:

- Initialize a new `uv` project
- Create a virtual environment inside `.venv/`
- Install all required Python dependencies from `requirements.txt`


### Hugging Face Token Setup

**Create a `.env` file** in the root directory and **Add your Hugging Face access token**:

```bash
echo "HF_TOKEN=Abc" > .env
```

Then, **print the content of the `.env` file to verify it**:
```bash
cat .env
```

***Please do not commit your api key to github, or share it with anyone online.**

### Launching the Local Model with vLLM

Before running the model startup script, you need to define execute permissions so it can be run as a program:

```bash
chmod +x start_model.sh
```

Use the provided script to launch the model server:

```bash
bash start_model.sh llama3-8b
```

**Available model keys:**

- `llama3-70b` (meta-llama/Meta-Llama-3-70B-Instruct)
- `llama3-8b`  (meta-llama/Meta-Llama-3-8B-Instruct)
- `mixtral`    (mistralai/Mixtral-8x7B-Instruct-v0.1)
- `qwen25-7b`  (Qwen/Qwen2.5-7B-Instruct)
- `qwen2-72b`  (Qwen/Qwen2-72B-Instruct)

**This will:**

- Load `.env`
- Verify GPU availability
- Set `MODEL_NAME` in `.env`
- Download the model to `.cache/models/<model_key>`
- Start the vLLM server at [http://localhost:8000/v1](http://localhost:8000/v1)

> ℹ️ **Note:** Additional models can be added by editing the `start_model.sh` script and updating the `MODEL_REGISTRY` and `TP_SIZES` sections accordingly.

### Testing the Model

Once the model server is running, you can test the model response by opening a **new terminal** and running:

```bash
uv run test_model.py
```
This script will:

- Load the model name from your `.env` file
- Send a sample prompt ("What is the capital of France?") to the local vLLM server
- Print the model's response to the console

> ⚠️ **Make sure the vLLM server is already running at** [http://localhost:8000/v1](http://localhost:8000/v1) **before executing the test.**


## Case Study

### Number Guessing Game 

To reproduce the results in the paper, please run the following command.

```bash
uv run main_number_guessing.py
```

You can specify additional parameters to reproduce the results of the paper.

The `<persona>` can be "default" (no persona), "aggressive", or "conservative".

The `<advanced>` option is used to specify advanced agent modeling options, including "domain_knowledge", "learning", "reasoning", "planning", and "hint" (conversation) discussed in the paper.

The `<set_guess_number>` is used to guess a fixed number.

The `<interpretation_guess>` is used for model interpretation.

```bash
uv run main_number_guessing.py --persona "conservative" --advanced "domain_knowledge" --set_guess_number --interpretation_guess
```

### Emergency Evacuation

To reproduce the results in the paper, please run the following command.

```bash
uv run main_emergency_evacuation.py --task <task_id>
```

The `<task_id>` can be one of the following options: [1, 2, 3, 4]. Each task id corresponds to a specific case study in the paper.

Additionally, if you would like to specify a seed, the number of humans, and add obstacles in the environment, you may want to run the following command.

```bash
uv run main_emergency_evacuation.py --task <task_id> --seed <seed> --num_humans <num_humans> --need_obstacle
```


### Plea Bargaining

To reproduce the results in the paper, please run the following command.

```bash
uv run main_plea_bargain.py
```

We provide a GUI to set the parameters of the run.

```bash
uv run main_plea_bargain.py --gui
```

If you choose to use command instead of the GUI to set the parameters for simulation, you may want to run the following command.

The `<persona>` can be "persona" or "nopersona", indicating whether or not the persona is used in the performance of plea bargaining.

The `<no_fewshot>` option indicates not to provide a few-shot context to the agent in the plea bargain.

The `<task>` can be one of the following options: [1, 2, 3]. Each task id corresponds to a specific case study in the paper.

```bash
uv run main_plea_bargain.py --tcu_test --persona "nopersona" --no_fewshot --output_max_tokens 100 --num_agents 1 --task 1
```

### Firm Pricing Competition


To reproduce the results in the paper, please run the following command.

```bash
uv run main_firm_pricing_competition.py
```

We provide a GUI to set the parameters of the run.

```bash
uv run main_firm_pricing_competition.py --gui
```

If you choose to use command instead of the GUI to set the parameters for simulation, you may want to run the following command.
The `<persona_firm>` parameter accepts one of the following options: [0, 1, 2]. Here, 0 indicates no persona, 1 represents an active persona, and 2 denotes an aggressive persona.

```bash
uv run main_firm_pricing_competition.py --rounds 1000 --output_max_tokens 100 --breakpoint_rounds 20 --persona_firm1 1 --persona_firm2 1 --set_initial_price --cost 2 2 --parameter_a 14 --parameter_d 0.00333333333333 --parameter_beta 0.00666666666666 --initial_price 2 2 --load_data_location "Record-231112-1955" --strategy --has_conversation
```

