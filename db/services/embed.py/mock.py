import random
from typing import List
from langchain_core.embeddings import Embeddings

class MockEmbeddingService(Embeddings):
    def __init__(self, dim: int = 384):
        self.dim = dim

    def get_embedding(self, text: str) -> List[float]:
        random.seed(hash(text) % 10000)  # determinismo débil
        return [random.random() for _ in range(self.dim)]

    def embed_documents(self, text: str) -> List[List[float]]:
        return [self.get_embedding(text)]

    def embed_query(self, text: str) -> List[float]:
        return self.get_embedding(text)
