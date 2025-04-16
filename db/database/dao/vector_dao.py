# database/dao/vector_dao.py
from typing import List
from pydantic import BaseModel
from .base_dao import BaseDAO

class VectorDAO(BaseDAO):
    def insert_data(self, data: BaseModel) -> str:
        """
        Inserta en la base de datos cualquier dato que sea instancia de un modelo Pydantic.
        
        :param data: Una instancia de Pydantic (p.ej., MinimalChunkModel, IndexedChunkModel, EnrichedChunkModel, etc.)
        :return: El identificador del documento insertado en la colección.
        """
        result = self.collection.insert_one(data.model_dump())
        return str(result.inserted_id)

    def vector_search(self, query_embedding: List[float], limit: int = 10) -> List[dict]:
        """
        Realiza una búsqueda vectorial sobre el campo 'embedding' de los documentos insertados.
        
        :param query_embedding: Vector de consulta.
        :param limit: Número máximo de resultados a retornar.
        :return: Lista de documentos que cumplen con el criterio de búsqueda.
        """
        pipeline = [
            {
                "$vectorSearch": {
                    "index": "vector_index",
                    "queryVector": query_embedding,
                    "path": "embedding",
                    "numCandidates": 100,
                    "limit": limit
                }
            }
        ]
        return list(self.collection.aggregate(pipeline))
