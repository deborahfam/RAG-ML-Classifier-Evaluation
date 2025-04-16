# document_processor.py
from typing import List
from chunking_strategies import (
    ChunkingStrategy, FixedLengthStrategy, OverlappingStrategy,
    SentenceBasedStrategy, ParagraphBasedStrategy, TokenBasedStrategy
)

class DocumentProcessor:
    def __init__(self, strategy: ChunkingStrategy):
        """
        :param strategy: Estrategia de chunking que se utilizará para procesar los documentos.
        """
        self.strategy = strategy

    def set_strategy(self, strategy: ChunkingStrategy):
        """
        Permite cambiar la estrategia de chunking en tiempo de ejecución.
        """
        self.strategy = strategy

    def process_document(self, text: str) -> List[str]:
        """
        Aplica la estrategia de chunking al texto y devuelve la lista de chunks generados.
        """
        return self.strategy.chunk(text)
