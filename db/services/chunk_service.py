# services/chunk_service.py
import uuid
from db.models.document_model import MinimalChunkModel, IndexedChunkModel, EnrichedChunkModel
from db.database.dao.vector_dao import VectorDAO
from utils.encoder import BaseEncoder

class ChunkService:
    def __init__(self, encoder: BaseEncoder):
        self.dao = VectorDAO()  # DAO encargado de las operaciones en MongoDB
        self.encoder = encoder

    def process_and_save_minimal_chunk(self, text: str, metadata: dict = None) -> str:
        """
        Procesa un chunk con el modelo MinimalChunkModel (solo texto, embedding y metadatos)
        y lo guarda en la base de datos.
        Retorna el identificador asignado en la BD.
        """
        embedding = self.encoder.encode(text)
        chunk = MinimalChunkModel(
            text=text,
            embedding=embedding,
            metadata=metadata or {}
        )
        return self.dao.insert_data(chunk)

    def process_and_save_indexed_chunk(self, document_id: str, text: str,
                                       start_index: int, end_index: int,
                                       page_number: int = None, metadata: dict = None) -> str:
        """
        Procesa un chunk utilizando el modelo IndexedChunkModel, incluyendo información
        de posición en el documento original.
        """
        embedding = self.encoder.encode(text)
        chunk = IndexedChunkModel(
            document_id=document_id,
            text=text,
            embedding=embedding,
            start_index=start_index,
            end_index=end_index,
            page_number=page_number,
            metadata=metadata or {}
        )
        return self.dao.insert_data(chunk)

    def process_and_save_enriched_chunk(self, document_id: str, text: str,
                                        start_index: int, end_index: int,
                                        summary: str = None, language: str = None,
                                        tags: list = None, section: str = None,
                                        sentiment: str = None, metadata: dict = None) -> str:
        """
        Procesa un chunk utilizando el modelo EnrichedChunkModel, incluyendo
        información adicional como resumen, idioma, etiquetas, etc.
        """
        embedding = self.encoder.encode(text)
        chunk = EnrichedChunkModel(
            document_id=document_id,
            text=text,
            embedding=embedding,
            start_index=start_index,
            end_index=end_index,
            summary=summary,
            language=language,
            tags=tags or [],
            section=section,
            sentiment=sentiment,
            metadata=metadata or {}
        )
        return self.dao.insert_data(chunk)

    def get_chunk_by_id(self, chunk_id: str):
        """
        Obtiene un chunk desde la base de datos dado su identificador.
        """
        return self.dao.get_chunk_by_id(chunk_id)

    def search_chunks_by_embedding(self, embedding: list, k: int = 5):
        """
        Realiza una búsqueda de chunks en la base de datos usando el embedding.
        Retorna una lista de los k chunks más cercanos.
        """
        return self.dao.search_chunks_by_embedding(embedding, k)
