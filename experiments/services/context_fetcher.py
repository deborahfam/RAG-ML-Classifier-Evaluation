from db.services.chunk_service import ChunkService
from langchain_core.embeddings import Embeddings

def fetch_context_from_query(query_embedding: list[float], limit: int = 3) -> str:
    embedder = Embeddings()
    chunk_service = ChunkService(embedder)
    results = chunk_service.dao.vector_search(query_embedding, limit=limit)
    context_chunks = [doc.get("text", "") for doc in results]
    return "\n---\n".join(context_chunks)
