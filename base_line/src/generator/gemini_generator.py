# services/generator/gemini_generator.py
import os
from dotenv import load_dotenv
import google.generativeai as genai
from .base import BaseGenerator

load_dotenv()

class GeminiGenerator(BaseGenerator):
    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.client = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                    generation_config={
                    "response_mime_type": "application/json"
                    }
                )

    def generate_text(self, prompt, model_name="gemini-1.5-flash", temperature=0.7, top_p=0.9):
        try:
            currentclient = self.client.GenerativeModel(
                model_name=model_name,
                    generation_config={
                    "response_mime_type": "text/plain",
                    "temperature": temperature,
                    "top_p": top_p
                    }
                )
            response = currentclient.generate_content(
                contents=prompt
            )
            return response.text
        except Exception as e:
            print(f"[GeminiTextGenerator] Error: {e}")
            return f"Error: {e}"

    def generate_json(self, prompt, model_name="gemini-1.5-flash", temperature=0.7, top_p=0.9):
        try:
            # currentclient = self.client.GenerativeModel(
            #     model_name=model_name,
            #         generation_config={
            #         "response_mime_type": "application/json",
            #         "temperature": temperature,
            #         "top_p": top_p
            #         }
            #         )
            
            response = self.client.generate_content(
                contents=prompt
            )
            return response.text # You can parse if needed
        except Exception as e:
            print(f"[GeminiTextGenerator] Error in JSON generation: {e}")
            return {"error": str(e)}
