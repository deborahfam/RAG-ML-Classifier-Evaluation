# indexers/vector_indexer.py
from database.connection import MongoDBConnection

class VectorIndexer:
    def __init__(self):
        self.collection = MongoDBConnection().get_collection()

    def create_vector_index(self):
        index_spec = {
            'name': 'vector_index',
            'type': 'vector',
            'fields': [{
                'name': 'embedding',
                'dimensions': 768,  # Ajustar según tu modelo
                'similarity': 'cosine'
            }]
        }
        return self.collection.create_search_index(index_spec)