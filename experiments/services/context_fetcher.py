import json
from typing import List
from db.services.chunk_service import ChunkService
from experiments.services.embedder.lmstudio import LMStudioEmbeddingService
import numpy as np

def fetch_context_from_query(query_embedding: list[float], limit: int = 3) -> str:
    embedder = LMStudioEmbeddingService()
    chunk_service = ChunkService(embedder)
    results = chunk_service.dao.vector_search(query_embedding, limit=limit)
    # print(results)
    context_chunks = [doc.get("text", "") for doc in results]
    return "\n---\n".join(context_chunks)

def load_context(file_path: str) -> List[str]:
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return [item['context_used'] for item in data]


def cosine_similarity(vec1, vec2):
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    if np.linalg.norm(vec1) == 0 or np.linalg.norm(vec2) == 0:
        return 0.0
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

def fetch_context_from_query_by_hand(query_embedding: list[float], limit: int = 3) -> str:
    embedder = LMStudioEmbeddingService()
    chunk_service = ChunkService(embedder)

    # Recuperar todos los documentos con campo 'embedding'
    all_docs = chunk_service.dao.collection.find(
        {"embedding": {"$exists": True}},
        {"text": 1, "embedding": 1}
    )

    # Calcular similitud coseno
    scored_docs = []
    for doc in all_docs:
        embedding = doc.get("embedding", [])
        score = cosine_similarity(query_embedding, embedding)
        scored_docs.append((score, doc))

    # Ordenar por similitud descendente y tomar los mejores 'limit'
    top_docs = sorted(scored_docs, key=lambda x: x[0], reverse=True)[:limit]

    # Extraer los textos
    context_chunks = [doc.get("text", "") for _, doc in top_docs]
    return "\n---\n".join(context_chunks)
