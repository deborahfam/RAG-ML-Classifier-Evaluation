import os
import uuid
from typing import Dict
import sys
from pathlib import Path
project_root = Path(__file__).resolve().parent.parent.parent  # Ajusta según tu estructura
sys.path.append(str(project_root))
from document_parser.services.pdf_loader import PDFLoader
from chunking_strategies import (
    FixedLengthStrategy,
    OverlappingStrategy,
    SentenceAwareFixedLengthStrategy,
    SentenceBasedStrategy,
    ParagraphBasedStrategy,
    TokenBasedStrategy,
)
from langchain_core.embeddings import Embeddings
from document_parser.models.chunks_model import IndexedChunkModel
from db.database.dao.vector_dao import VectorDAO
from document_processor import DocumentProcessor
from services.embedder.lmstudio import LMStudioEmbeddingService
from services.embedder.fireworks import FireworksEmbeddingService
class PDFProcessingPipeline:
    def __init__(
        self,
        pdf_dir: str,
        chunking_strategy: str = "sentence",
        chunk_params: Dict = None,
        text_backend: str = "pypdf",  # Puede ser "pymupdf4llm" o "pypdf"
    ):
        self.loader = PDFLoader(pdf_dir, backend=text_backend)
        self.embedder = LMStudioEmbeddingService()
        # self.embedder = FireworksEmbeddingService()
        self.dao = VectorDAO()
        self.processor = DocumentProcessor(
            self._get_strategy(chunking_strategy, chunk_params or {})
        )

    def _get_strategy(self, name: str, params: Dict):
        strategies = {
            "fixed": lambda p: FixedLengthStrategy(p.get("chunk_size", 500)),
            "overlap": lambda p: OverlappingStrategy(p.get("chunk_size", 500), p.get("overlap", 100)),
            "sentence": lambda p: SentenceBasedStrategy(p.get("max_chunk_size", 500)),
            "paragraph": lambda p: ParagraphBasedStrategy(),
            "token": lambda p: TokenBasedStrategy(p.get("chunk_tokens", 200), p.get("step_tokens", 100)),
            "fixed_sentence": lambda p: SentenceAwareFixedLengthStrategy(max_chunk_size=2000)
        }
        if name not in strategies:
            raise ValueError(f"Estrategia de chunking no válida: {name}")
        return strategies[name](params)

    def process_pdfs(self):
        for pdf_path in self.loader.get_pdf_files():
            document_id = os.path.splitext(os.path.basename(pdf_path))[0]
            pages = self.loader.extract_pages(pdf_path)

            for page_number, text in pages:
                chunks = self.processor.process_document(text)
                self._store_chunks(document_id, page_number, text, chunks)

    def _store_chunks(self, document_id, page_number, full_text, chunks):
        cursor = 0
        for chunk_text in chunks:
            start_idx = full_text.find(chunk_text, cursor)
            if start_idx == -1:
                continue  # Skip if not found
            end_idx = start_idx + len(chunk_text)
            cursor = end_idx

            embedding = self.embedder.get_embedding(chunk_text)
            chunk_id = str(uuid.uuid4())

            model = IndexedChunkModel(
                chunk_id=chunk_id,
                document_id=document_id,
                text=chunk_text,
                embedding=embedding,
                start_index=start_idx,
                end_index=end_idx,
                length=len(chunk_text),
                page_number=page_number,
                metadata={},
            )
            self.dao.insert_data(model)
