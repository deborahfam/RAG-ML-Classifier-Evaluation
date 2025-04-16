from pydantic import BaseModel
from typing import List, Optional, Dict

class IndexedChunkModel(BaseModel):
    chunk_id: str
    document_id: str
    text: str
    embedding: List[float]
    start_index: int
    end_index: int
    length: Optional[int]
    page_number: Optional[int]
    metadata: Optional[Dict] = {}