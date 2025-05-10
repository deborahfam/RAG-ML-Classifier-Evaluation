import json
import requests
from typing import Any, Dict
from services.generator.base import BaseGenerator


class LMStudioGenerator(BaseGenerator):
    def __init__(self, base_url: str = "http://localhost:1234/v1/chat/completions"):
        self.base_url = base_url

    def _call_lm_studio(
        self, prompt: str, model_name: str, temperature: float, top_p: float, max_tokens: int = 1000
    ) -> str:
        payload = {
            "model": model_name,
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            "temperature": temperature,
            "top_p": top_p,
            "stream": False,
            # "max_tokens": max_tokens,
        }

        response = requests.post(self.base_url, json=payload)
        response.raise_for_status()

        result = response.json()
        return result["choices"][0]["message"]["content"]

    def generate_text(
        self, prompt: str, model_name: str, temperature: float = 0.7, top_p: float = 0.9, max_tokens: int = 1000
    ) -> str:
        return self._call_lm_studio(prompt, model_name, temperature, top_p, max_tokens=max_tokens)

    def generate_json(
        self, prompt: str, model_name: str, temperature: float = 0.7, top_p: float = 0.9, max_tokens: int = 1000
    ) -> dict:
        response_text = self._call_lm_studio(prompt, model_name, temperature, top_p, max_tokens=max_tokens)

        return response_text
