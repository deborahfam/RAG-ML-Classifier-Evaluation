import os
from openai import OpenAI
import requests
from typing import List
from langchain_core.embeddings import Embeddings

class LMStudioEmbeddingService(Embeddings):
    def __init__(self):
        self.client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

    def get_embedding(self, text: str, model: str = "text-embedding-nomic-embed-text-v1.5") -> List[float]:
        return self.client.embeddings.create(input=[text], model=model).data[0].embedding

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        # LM Studio puede procesar varios textos a la vez
        response = requests.post(
            self.base_url,
            json={
                "input": texts,
                "model": self.model
            }
        )
        response.raise_for_status()
        return [item["embedding"] for item in response.json()["data"]]

    def embed_query(self, text: str) -> List[float]:
        return self.get_embedding(text)
