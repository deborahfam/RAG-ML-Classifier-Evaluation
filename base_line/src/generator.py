import streamlit as st
from openai import OpenAI
from config import API_BASE, API_KEY
from db.utils.encoder import OpenAIEmbeddingEncoder
from prompt import BASELINE_TEMPLATE

class GeneratorService:
    def __init__(self) -> None:
        self.client = OpenAI(
            base_url=API_BASE, 
            api_key=API_KEY
        )

    def text_generator(self, model_name, temperature, top_p, query):
        prompt = BASELINE_TEMPLATE.replace("query", query)
        messages = [{"role": "user", "content": prompt}]
        return self.client.chat.completions.create(
            model=model_name,
            messages=messages,
            stream=True,
            temperature=temperature,
            top_p=top_p,
        )
    
    def json_generator(self, model_name, temperature, top_p, query):
        prompt = BASELINE_TEMPLATE.replace("query", query)
        messages = [{"role": "user", "content": prompt}]
        return self.client.chat.completions.create(
            model=model_name,
            messages=messages,
            stream=False,
            temperature=temperature,
            top_p=top_p,
            response_format={"type": "json_object"}
        )
