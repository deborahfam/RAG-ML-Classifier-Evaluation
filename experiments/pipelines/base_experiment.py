from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from ..services.generator.base import BaseGenerator
from langchain_core.embeddings import Embeddings
from ..services.context_fetcher import fetch_context_from_query

class BaseExperiment(ABC):
    def __init__(
        self,
        embedder: Embeddings,
        generator: BaseGenerator,
        strategy_name: str,
        model_name: str,
        min_score: float = 0.7,
        max_tokens: int = 2000
    ):
        self.embedder = embedder
        self.generator = generator
        self.strategy_name = strategy_name
        self.model_name = model_name
        self.min_score = min_score
        self.max_tokens = max_tokens

    @abstractmethod
    def build_prompt(self, context: str, query: str) -> str:
        """Build the prompt using the specific strategy"""
        pass

    def run(self, query: str) -> Dict[str, Any]:
        """Run the experiment with the given query"""
        # Get query embedding
        query_embedding = self.embedder.get_embedding(query)
        
        # Fetch relevant context
        context = fetch_context_from_query(
            query_embedding=query_embedding,
            min_score=self.min_score,
            max_tokens=self.max_tokens
        )
        
        # Build prompt using strategy
        prompt = self.build_prompt(context=context, query=query)
        
        # Generate response
        response = self.generator.generate_text(
            prompt=prompt,
            model_name=self.model_name
        )
        
        return {
            "strategy": self.strategy_name,
            "model": self.model_name,
            "query": query,
            "context": context,
            "prompt": prompt,
            "response": response
        } 