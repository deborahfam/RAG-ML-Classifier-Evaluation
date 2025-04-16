# services/document_service.py
from models.document_model import DocumentModel
from database.dao.vector_dao import VectorDAO
from utils.encoder import BaseEncoder  # Ahora usando nuestro encoder base

class DocumentService:
    def __init__(self, encoder: BaseEncoder):  # Inyectamos el encoder
        self.dao = VectorDAO()
        self.encoder = encoder

    def process_and_save_document(self, text: str, metadata: dict = None) -> str:
        embedding = self.encoder.encode(text)
        document = DocumentModel(
            text=text,
            embedding=embedding,
            metadata=metadata or {}
        )
        return self.dao.insert_document(document)