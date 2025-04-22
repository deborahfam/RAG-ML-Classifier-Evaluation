# services/generator/openai_generator.py
import os
from openai import OpenAI
from fireworks.client import Fireworks
from .base import BaseGenerator

class OpenAIGenerator(BaseGenerator):
    def __init__(self, use_fireworks=False):
        if use_fireworks:
            self.client = Fireworks(api_key=os.getenv("FIREWORKS_API_KEY"))
        else:
            self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def generate_text(self, prompt, model_name, temperature=0.7, top_p=0.9):
        try:
            messages = [{"role": "user", "content": prompt}]
            response = self.client.chat.completions.create(
                model=model_name,
                messages=messages,
                temperature=temperature,
                top_p=top_p,
                stream=False
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"[OpenAITextGenerator] Error: {e}")
            return f"Error: {e}"

    def generate_json(self, prompt, model_name, temperature=0.7, top_p=0.9):
        try:
            messages = [{"role": "user", "content": prompt}]
            response = self.client.chat.completions.create(
                model=model_name,
                messages=messages,
                temperature=temperature,
                top_p=top_p,
                stream=False,
                response_format={"type": "json_object"}
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"[OpenAITextGenerator] Error in JSON generation: {e}")
            return {"error": str(e)}
