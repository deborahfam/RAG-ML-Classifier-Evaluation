from typing import List
import os
import dotenv
import google.generativeai as genai
from langchain_core.embeddings import Embeddings
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type
import time

dotenv.load_dotenv()

class GeminiEmbeddingService(Embeddings):
    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel('embedding-001')  # o el que esté disponible

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_fixed(5),  # espera 5 segundos entre intentos
        retry=retry_if_exception_type(Exception)  # puedes personalizar solo para 429
    )
    def get_embedding(self, text: str) -> List[float]:
        response = self.model.embed_content(content=text, task_type="retrieval_document")
        return response['embedding']

    def embed_documents(self, text: str) -> List[List[float]]:
        return [self.get_embedding(text)]

    def embed_query(self, text: str) -> List[float]:
        return self.get_embedding(text)
