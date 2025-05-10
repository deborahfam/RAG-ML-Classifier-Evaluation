# services/generator/openai_generator.py
import os
from typing import Type, TypeVar
from openai import OpenAI
from pydantic import BaseModel
from experiments.json_formats.reasoning import ClassificationModel
from fireworks.client import Fireworks
from .base import BaseGenerator

T = TypeVar("T", bound=BaseModel)
class OpenAIGenerator(BaseGenerator):
    def __init__(self, use_fireworks=False):
        if use_fireworks:
            self.client = OpenAI(api_key=os.getenv("FIREWORKS_API_KEY"), base_url=os.getenv("FIREWORKS_API_BASE"))
        else:
            self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def generate_text(self, prompt, model_name, temperature=0.7, top_p=0.9):
        try:
            messages = [{"role": "user", "content": prompt}]
            response = self.client.chat.completions.create(
                model=model_name,
                messages=messages,
                stream=False
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"[OpenAITextGenerator] Error: {e}")
            return f"Error: {e}"

    def generate_json(self, model, prompt, json_model: Type[T], **kwargs) -> BaseModel:
        messages = [{"role": "user", "content": prompt}]
        response = self.client.beta.chat.completions.parse(
            model=model,
            messages=messages,
            response_format=json_model,
            temperature=0,
            **kwargs,
        )
        # print(response)
        return response
