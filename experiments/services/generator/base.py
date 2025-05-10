# services/generator/base.py
from abc import ABC, abstractmethod
from typing import Type

from pydantic import BaseModel

class BaseGenerator(ABC):
    @abstractmethod
    def generate_text(self, prompt: str, model_name: str, temperature: float = 0.7, top_p: float = 0.9) -> str:
        pass

    @abstractmethod
    def generate_json(self, prompt: str, model_name: str, json_model: Type[BaseModel], temperature: float = 0.7, top_p: float = 0.9) -> dict:
        pass
