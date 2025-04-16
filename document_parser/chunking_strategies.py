# chunking_strategies.py
import re
from abc import ABC, abstractmethod
from typing import List

class ChunkingStrategy(ABC):
    @abstractmethod
    def chunk(self, text: str) -> List[str]:
        """
        Recibe el texto y lo divide en una lista de chunks según la estrategia implementada.
        """
        pass

class FixedLengthStrategy(ChunkingStrategy):
    def __init__(self, chunk_size: int):
        """
        :param chunk_size: Tamaño de cada chunk en número de caracteres.
        """
        self.chunk_size = chunk_size

    def chunk(self, text: str) -> List[str]:
        """
        Divide el texto en segmentos de longitud fija.
        """
        return [text[i:i + self.chunk_size] for i in range(0, len(text), self.chunk_size)]

class OverlappingStrategy(ChunkingStrategy):
    def __init__(self, chunk_size: int, overlap: int):
        """
        :param chunk_size: Longitud de cada chunk en caracteres.
        :param overlap: Número de caracteres de superposición entre chunks consecutivos.
        """
        if overlap >= chunk_size:
            raise ValueError("El overlap debe ser menor que el chunk_size")
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(self, text: str) -> List[str]:
        """
        Divide el texto en chunks de longitud fija, con una parte superpuesta entre ellos.
        """
        chunks = []
        step = self.chunk_size - self.overlap
        for i in range(0, len(text), step):
            chunk = text[i:i + self.chunk_size]
            if chunk:
                chunks.append(chunk)
        return chunks

class SentenceBasedStrategy(ChunkingStrategy):
    def __init__(self, max_chunk_size: int):
        """
        :param max_chunk_size: Tamaño máximo de un chunk (en caracteres) formado por oraciones.
        """
        self.max_chunk_size = max_chunk_size

    def chunk(self, text: str) -> List[str]:
        """
        Separa el texto en oraciones y agrupa oraciones en chunks sin sobrepasar el tamaño máximo.
        """
        import re
        # Separa en oraciones usando una expresión regular simple.
        sentences = re.split(r'(?<=[.!?])\s+', text)
        chunks = []
        current_chunk = ""
        for sentence in sentences:
            if len(current_chunk) + len(sentence) + 1 <= self.max_chunk_size:
                current_chunk = f"{current_chunk} {sentence}".strip() if current_chunk else sentence
            else:
                if current_chunk:
                    chunks.append(current_chunk)
                current_chunk = sentence
        if current_chunk:
            chunks.append(current_chunk)
        return chunks

class ParagraphBasedStrategy(ChunkingStrategy):
    def chunk(self, text: str) -> List[str]:
        """
        Divide el texto en párrafos asumiendo que están separados por dos saltos de línea.
        """
        # Elimina espacios en blanco adicionales y filtra párrafos vacíos.
        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
        return paragraphs

class TokenBasedStrategy(ChunkingStrategy):
    def __init__(self, chunk_tokens: int, step_tokens: int):
        """
        :param chunk_tokens: Número de tokens (palabras) que debe tener cada chunk.
        :param step_tokens: Número de tokens que se desplaza la ventana en cada iteración.
        """
        self.chunk_tokens = chunk_tokens
        self.step_tokens = step_tokens

    def chunk(self, text: str) -> List[str]:
        """
        Aplica una ventana deslizante sobre los tokens del texto para generar chunks.
        """
        tokens = text.split()
        chunks = []
        for i in range(0, len(tokens), self.step_tokens):
            chunk_tokens = tokens[i:i + self.chunk_tokens]
            if chunk_tokens:
                chunks.append(" ".join(chunk_tokens))
        return chunks

class SentenceAwareFixedLengthStrategy:
    def __init__(self, max_chunk_size: int):
        """
        :param max_chunk_size: Tamaño máximo de cada fragmento en caracteres.
        """
        self.max_chunk_size = max_chunk_size

    def chunk(self, text: str) -> List[str]:
        """
        Divide el texto en fragmentos que no excedan max_chunk_size y que terminen en el final de una oración.
        """
        # Dividir el texto en oraciones utilizando una expresión regular.
        sentences = re.split(r'(?<=[.!?])\s+', text)
        chunks = []
        current_chunk = ""

        for sentence in sentences:
            if len(current_chunk) + len(sentence) + 1 <= self.max_chunk_size:
                # Agregar la oración al fragmento actual.
                current_chunk = f"{current_chunk} {sentence}".strip() if current_chunk else sentence
            else:
                # Guardar el fragmento actual y comenzar uno nuevo.
                if current_chunk:
                    chunks.append(current_chunk)
                current_chunk = sentence

        # Agregar el último fragmento si existe.
        if current_chunk:
            chunks.append(current_chunk)

        return chunks
