import base64
import json
from typing import List, Tuple
from PyPDF2 import PdfReader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from services.db.models import DocumentPageModel, DocumentMetadataModel
from services.db.mongodb import MongoDBService
from services.embeddings import EmbeddingService
from config import collection, db
import nltk
import hashlib
from services.main import MainService
import re
import io
import pymupdf4llm
import pymupdf


from prompts import (
    GENERATE_QUESTIONS,
    GENERATE_IDEAS,
    GENERATE_SUMMARIZE,
)
from PIL import Image

class DocumentProcessorService:
    def __init__(self, embedding_model: EmbeddingService) -> None:
        self.embedding_model = embedding_model
        self.handler = MainService(embedding_model=embedding_model)
        self.model = "accounts/fireworks/models/mixtral-8x7b-instruct"
        self.recursive_text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2000, chunk_overlap=20
        )
        self.db_handler = MongoDBService()

    def embed_text(self, chunk_text: str):
        """Embed the chunk of text using the embedding model."""
        return self.embedding_model.embed_documents(chunk_text)


    def process_and_save(self, file):
        pdf_file = pymupdf.open(stream=file.read())
        md_text_chunks = pymupdf4llm.to_markdown(
            pdf_file, page_chunks=True, write_images=False
        )

        for chunk in md_text_chunks:
            print("isduplicate", self.is_duplicate(chunk["text"]), flush=True)
            if not self.is_duplicate(chunk["text"]):
                # metadata_id = self.process_metadata(chunk)

                document_data = DocumentPageModel(
                    hash_code=hashlib.sha256(chunk["text"].encode("utf-8")).hexdigest(),
                    document_title=pdf_file.name,
                    document_name=pdf_file.name,  # TODO change this to the pdf path
                    total_pages=len(md_text_chunks),
                    page=chunk["metadata"]["page"],
                    page_text=chunk["text"],
                    page_text_embedded=self.embed_text(chunk["text"]),
                    # metadata_id=metadata_id,
                )
                self.db_handler.insert_one(
                    "docs", document_data.model_dump(by_alias=True)
                )

    def is_duplicate(self, text: str) -> bool:
        """Check if the text content already exists in the database."""
        hash_digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
        existing_document = db["docs"].find_one(
            {"hash_code": hash_digest}
        )
        return existing_document is not None
