# tests/test_document_processor.py
from document_processor import DocumentProcessor
from chunking_strategies import (
    FixedLengthStrategy,
    OverlappingStrategy,
    SentenceBasedStrategy,
    ParagraphBasedStrategy,
    TokenBasedStrategy
)
import sys
from pathlib import Path

# Añade la ruta del proyecto al sys.path
project_root = Path(__file__).resolve().parent.parent.parent  # Ajusta según tu estructura
sys.path.append(str(project_root))
from db.utils.encoder import BaseEncoder
from db.database.dao.vector_dao import VectorDAO
from db.models.document_model import MinimalChunkModel

# Implementación de un encoder dummy para pruebas
class DummyEncoder(BaseEncoder):
    def encode(self, text: str) -> list:
        # Retorna un vector simple basado en la longitud del texto (vector fijo de 4 dimensiones)
        return [float(len(text))] * 4

if __name__ == '__main__':
    # Documento de ejemplo
    sample_text = (
        "Este es un documento de prueba. Se utiliza para demostrar la funcionalidad "
        "de chunking. El documento será segmentado en diferentes partes según la "
        "estrategia escogida, y cada uno de esos chunks se almacenará en la base de datos."
    )
    document_id = "doc_test_001"
    
    # Definición de las estrategias disponibles
    strategies = {
        "FixedLengthStrategy": FixedLengthStrategy(chunk_size=50),
        "OverlappingStrategy": OverlappingStrategy(chunk_size=50, overlap=10),
        "SentenceBasedStrategy": SentenceBasedStrategy(max_chunk_size=100),
        "ParagraphBasedStrategy": ParagraphBasedStrategy(),
        "TokenBasedStrategy": TokenBasedStrategy(chunk_tokens=10, step_tokens=5)
    }
    
    # Instancia del encoder dummy y del DAO para persistencia
    encoder = DummyEncoder()
    dao = VectorDAO()
    
    # Procesamiento del documento para cada estrategia
    for strategy_name, strategy in strategies.items():
        print(f"\n===== Usando estrategia: {strategy_name} =====")
        processor = DocumentProcessor(strategy=strategy)
        chunks = processor.process_document(sample_text)
        
        print(f"Se han generado {len(chunks)} chunks:")
        for i, chunk in enumerate(chunks, start=1):
            print(f"  Chunk {i}: {chunk}")
        
        # Por cada chunk generado, se calcula su embedding, se crea una instancia de MinimalChunkModel
        # y se inserta en la base de datos.
        chunk_ids = []
        for chunk_text in chunks:
            embedding = encoder.encode(chunk_text)
            # Se incluye información adicional en el metadata, como el id del documento y la estrategia utilizada.
            model = MinimalChunkModel(
                text=chunk_text,
                embedding=embedding,
                metadata={"document_id": document_id, "strategy": strategy_name}
            )
            inserted_id = dao.insert_data(model)
            chunk_ids.append(inserted_id)
        
        print("IDs de chunks insertados:", chunk_ids)
