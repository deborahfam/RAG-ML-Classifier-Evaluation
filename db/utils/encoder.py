# utils/encoder.py
from typing import List, Union
import os
import dotenv
from openai import OpenAI
from abc import ABC, abstractmethod
from pydantic import BaseModel

dotenv.load_dotenv()

class BaseEncoder(ABC):
    @abstractmethod
    def encode(self, text: str) -> List[float]:
        pass

class OpenAIEmbeddingEncoder(BaseEncoder):
    def __init__(self):
        self.client = OpenAI(
            base_url=os.getenv("FIREWORKS_API_BASE"), 
            api_key=os.getenv("FIREWORKS_API_KEY")
        )
        self.model = os.getenv("EMBEDDING_MODEL")

    def encode(self, text: str) -> List[float]:
        """Implementación requerida por BaseEncoder"""
        return self._get_embedding(text)

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Para múltiples documentos (batch)"""
        response = self.client.embeddings.create(
            input=texts,
            model=self.model
        )
        return [embedding.embedding for embedding in response.data]

    def embed_query(self, text: str) -> List[float]:
        """Para consultas individuales"""
        return self.encode(text)
    
class DummyEncoder(BaseEncoder):
    def encode(self, text: str) -> List[float]:
        # Retorna un vector simple basado en la longitud del texto
        return [float(len(text))] * 4