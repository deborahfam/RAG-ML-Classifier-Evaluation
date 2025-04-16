# models/document_model.py
from pydantic import BaseModel
from typing import Dict, List, Optional
from datetime import datetime

class MinimalChunkModel(BaseModel):
    text: str
    embedding: List[float]
    metadata: Optional[Dict] = {}

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

class EnrichedChunkModel(BaseModel):
    chunk_id: str
    document_id: str
    text: str
    embedding: List[float]
    start_index: int
    end_index: int
    length: int
    summary: Optional[str] = None
    language: Optional[str] = None
    tags: List[str] = []
    section: Optional[str] = None
    sentiment: Optional[str] = None
    metadata: Optional[Dict] = {}