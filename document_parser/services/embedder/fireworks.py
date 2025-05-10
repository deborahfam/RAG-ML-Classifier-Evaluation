from typing import List
import dotenv
import os
from openai import OpenAI
from langchain_core.embeddings import Embeddings
from fireworks.client import Fireworks
dotenv.load_dotenv()

class FireworksEmbeddingService(Embeddings):
    def __init__(self):
        # self.client = OpenAI(
        #     base_url=os.getenv("FIREWORKS_API_BASE"), 
        #     api_key=os.getenv("FIREWORKS_API_KEY")
        # )
        self.client = Fireworks(
            base_url=os.getenv("FIREWORKS_API_BASE"),
            api_key=os.getenv("FIREWORKS_API_KEY")
        )

    def get_embedding(self, text: str, model: str = "nomic-ai/nomic-embed-text-v1.5") -> List[float]:
        return self.client.embeddings.create(input=[text], model=model).data[0].embedding

    def embed_documents(self, text: str) -> List[List[float]]:
        return [self.get_embedding(text)]

    def embed_query(self, text: str) -> List[float]:
        return self.get_embedding(text)
