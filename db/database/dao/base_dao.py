# database/dao/base_dao.py
import sys
from pathlib import Path

# Añade la ruta del proyecto al sys.path
project_root = Path(__file__).resolve().parent.parent  # Ajusta según tu estructura
sys.path.append(str(project_root))
from db.database.connection import MongoDBConnection

class BaseDAO:
    def __init__(self):
        self.collection = MongoDBConnection().get_collection()