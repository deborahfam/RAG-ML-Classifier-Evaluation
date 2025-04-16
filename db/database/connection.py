# database/connection.py
import sys
from pathlib import Path

# Añade la ruta del proyecto al sys.path
project_root = Path(__file__).resolve().parent.parent  # Ajusta según tu estructura
sys.path.append(str(project_root))
from pymongo import MongoClient
from db.config.settings import settings

class MongoDBConnection:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls.client = MongoClient(settings.mongo_uri)
            cls.db = cls.client[settings.db_name]
        return cls._instance

    def get_collection(self):
        return self.db[settings.collection_name]