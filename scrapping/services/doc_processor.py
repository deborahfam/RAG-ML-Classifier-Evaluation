from typing import List, Tuple
from PyPDF2 import PdfReader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from services.db.mongodb import MongoDBService
from services.embeddings import EmbeddingService
import hashlib
import pymupdf4llm
import pymupdf
import os
import dotenv

dotenv.load_dotenv()

# Environment Variables
DB_NAME = os.getenv("DB_NAME")
DOCUMENT_PAGE_COLLECTION = os.getenv("DOCUMENT_PAGE_COLLECTION")
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "2000"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "20"))

class DocumentProcessorService:
    def __init__(self, embedding_model: EmbeddingService) -> None:
        self.embedding_model = embedding_model
        self.recursive_text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP
        )
        self.db_handler = MongoDBService()

    def embed_text(self, chunk_text: str):
        """Embed the chunk of text using the embedding model."""
        return self.embedding_model.embed_documents(chunk_text)

    def process_and_save(self, file):
        """Process PDF file and save chunks to database."""
        pdf_file = pymupdf.open(stream=file.read())
        md_text_chunks = pymupdf4llm.to_markdown(
            pdf_file, page_chunks=True, write_images=False
        )

        for chunk in md_text_chunks:
            if not self.is_duplicate(chunk["text"]):
                chunk_text = chunk["text"]
                chunk_embedding = self.embed_text(chunk_text)

                # Save the chunk with the same structure as web crawler
                self.db_handler.save_document(
                    url=f"pdf://{pdf_file.name}",  # Using pdf:// prefix to distinguish from web URLs
                    chunk_text=chunk_text,
                    embedding=chunk_embedding,
                    metadata={
                        "source_type": "pdf",
                        "document_title": pdf_file.name,
                        "page": chunk["metadata"]["page"],
                        "total_pages": len(md_text_chunks)
                    }
                )

    def is_duplicate(self, text: str) -> bool:
        """Check if the text content already exists in the database."""
        hash_digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
        existing_document = self.db_handler.find_one(
            DOCUMENT_PAGE_COLLECTION,
            {"hash_code": hash_digest}
        )
        return existing_document is not None

