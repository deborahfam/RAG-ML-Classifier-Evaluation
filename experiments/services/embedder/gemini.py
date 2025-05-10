from typing import List
import os
import dotenv
# import google.generativeai as genai
from google import genai
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type
import time

dotenv.load_dotenv()

class GeminiEmbeddingService():
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_fixed(5),  # espera 5 segundos entre intentos
        retry=retry_if_exception_type(Exception)  # puedes personalizar solo para 429
    )
    def get_embedding(self, text: str) -> List[float]:
        result = self.client.models.embed_content(
        model="embedding-001",
        contents=text,
        # config=types.EmbedContentConfig(task_type="SEMANTIC_SIMILARITY")
        )
        return result.embeddings[0].values
    
    def embed_documents(self, text: str) -> List[List[float]]:
        return [self.get_embedding(text)]

    def embed_query(self, text: str) -> List[float]:
        return self.get_embedding(text)
