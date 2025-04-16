# fireworks_models.py

FIREWORKS_MODELS = {
    "Llama 4 Maverick Instruct": "accounts/fireworks/models/llama-v4-maverick",
    "Llama 4 Scout Instruct": "accounts/fireworks/models/llama-v4-scout",
    "Llama 3.1 405B Instruct": "accounts/fireworks/models/llama-3-405b-instruct",
    "DeepSeek R1 (Fast)": "accounts/fireworks/models/deepseek-r1",
    "DeepSeek V3": "accounts/fireworks/models/deepseek-v3",
    "FireFunction V1": "accounts/fireworks/models/firefunction-v1",
    "Mistral 7B Instruct": "accounts/fireworks/models/mistral-7b-instruct",
    "Mixtral 8x7B Instruct": "accounts/fireworks/models/mixtral-8x7b-instruct"
}
MODEL_CONFIGURATIONS = {
    "Llama 3.3 70B Instruct": {
        "model_name": "accounts/fireworks/models/llama-3.3-70b-instruct",
        "temperature": 0.7,
        "max_tokens": 500,
    },
    "Llama 3.1 405B Instruct": {
        "model_name": "accounts/fireworks/models/llama-3.1-405b-instruct",
        "temperature": 0.6,
        "max_tokens": 600,
    },
    "DeepSeek R1": {
        "model_name": "accounts/fireworks/models/deepseek-r1",
        "temperature": 0.5,
        "max_tokens": 700,
    },
    "DeepSeek V3": {
        "model_name": "accounts/fireworks/models/deepseek-v3",
        "temperature": 0.8,
        "max_tokens": 800,
    },
    "Llama 3.1 8B Instruct": {
        "model_name": "accounts/fireworks/models/llama-3.1-8b-instruct",
        "temperature": 0.9,
        "max_tokens": 900,
    },
    "DeepSeek R1 Distill Llama 8B": {
        "model_name": "accounts/fireworks/models/deepseek-r1-distill-llama-8b",
        "temperature": 0.4,
        "max_tokens": 400,
    },
}
