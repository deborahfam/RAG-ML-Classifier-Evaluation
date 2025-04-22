
# from openai import OpenAI
from openai import OpenAI
from fireworks.client import Fireworks
from dotenv import load_dotenv
import sys, os
from pathlib import Path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(project_root))

import google.generativeai as genai

load_dotenv()
class GeneratorService:
    def __init__(self) -> None:
        # self.client = OpenAI(
        #     base_url=os.getenv("FIREWORKS_API_BASE"), 
        #     api_key=os.getenv("FIREWORKS_API_KEY"))
        self.client = Fireworks(api_key=os.getenv("FIREWORKS_API_KEY"))

        # genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        # self.client = genai.GenerativeModel(
        #     model_name="gemini-1.5-flash",
        #         generation_config={
        #         "response_mime_type": "application/json"})

    # OPENAI based responses
    def openai_text_generator(self, model_name, temperature, top_p, prompt):
        messages = [{"role": "user", "content": prompt}]
        # print("messages: ", messages)
        try:
            return self.client.chat.completions.create(
                model=model_name,
                messages=messages,
                stream=False,
                # temperature=temperature,
                # top_p=top_p,
            ).choices[0].message.content
        except Exception as e:
            print(f"OpenAI API call failed: {e}")
            raise
    
    def openai_json_generator(self, model_name, temperature, top_p, prompt):
        messages = [{"role": "user", "content": prompt}]
        return self.client.chat.completions.create(
            model=model_name,
            messages=messages,
            stream=False,
            temperature=temperature,
            top_p=top_p,
            response_format={"type": "json_object"}
        )

    # GOOGLE based responses
    def gemini_text_generator(self, model_name, temperature, top_p, prompt):
        response = self.client.models.generate_content(
            model=model_name,
            contents=prompt,
            temperature=temperature,
            top_p=top_p,
            response_mime_type="text/plain",
        )
        return response.text
    
    def gemini_json_generator(self, model_name, temperature, top_p, prompt):
        response = self.client.generate_content(
            contents=prompt
        )
        return response.text

