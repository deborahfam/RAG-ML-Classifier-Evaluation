from typing import List
from sentence_transformers import SentenceTransformer
from langchain_core.embeddings import Embeddings

class HuggingFaceEmbeddingService(Embeddings):
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def get_embedding(self, text: str) -> List[float]:
        return self.model.encode(text).tolist()

    def embed_documents(self, text: str) -> List[List[float]]:
        return [self.get_embedding(text)]

    def embed_query(self, text: str) -> List[float]:
        return self.get_embedding(text)
