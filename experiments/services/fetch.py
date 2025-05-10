from typing import List
from openai import embeddings

from db.database.connection import MongoDBConnection


def fetch_context_from_query(embedder: embeddings, query: str, top_k: int = 3) -> List[str]:
    query_embedding = embedder.embed_query(query)
    collection = MongoDBConnection().get_collection()

    results = collection.aggregate([
        {
            "$vectorSearch": {
                "queryVector": query_embedding,
                "path": "embedding",
                "numCandidates": 100,
                "limit": top_k,
                "index": "vector_index"
            }
        },
        {
            "$project": {
                "text": 1,
                "_id": 0
            }
        }
    ])
    return [doc["text"] for doc in results]
