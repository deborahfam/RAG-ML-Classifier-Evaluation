# test_algorithm.py
from services.chunk_service import ChunkService
from utils.encoder import BaseEncoder

# Definición de un encoder "dummy" para propósitos de test
class DummyEncoder(BaseEncoder):
    def encode(self, text: str) -> list:
        # Por ejemplo, simplemente retornamos un vector donde cada componente es la longitud del texto.
        # Así, diferentes textos tendrán distintos vectores, aunque la lógica es muy básica.
        return [float(len(text))] * 4

if __name__ == '__main__':
    # Lista de textos de prueba
    textos = [
        "Este es el primer texto a procesar.",
        "Otro ejemplo de texto, con detalles adicionales para procesar y ver el funcionamiento.",
        "Prueba de texto corto."
    ]

    # Instanciamos nuestro encoder dummy
    encoder = DummyEncoder()

    # Creamos el servicio de chunks que utiliza el encoder y el DAO para MongoDB
    chunk_service = ChunkService(encoder)

    # Procesamos e insertamos cada texto como un chunk utilizando el modelo minimal
    ids_insertados = []
    for texto in textos:
        chunk_id = chunk_service.process_and_save_minimal_chunk(texto)
        ids_insertados.append(chunk_id)
        print(f"Chunk insertado con id: {chunk_id} para el texto: \"{texto}\"")

    # Para probar la búsqueda vectorial:
    # Tomamos el primer texto y obtenemos su embedding usando el encoder
    embedding_de_prueba = encoder.encode(textos[0])

    # Realizamos una búsqueda vectorial en la base de datos utilizando el embedding
    resultados_busqueda = chunk_service.dao.vector_search(embedding_de_prueba, limit=3)
    print("\nResultados de la búsqueda vectorial:")
    for resultado in resultados_busqueda:
        print(resultado)
