from abc import ABC, abstractmethod

class BasePromptPipeline(ABC):
    """
    Define cómo generar el prompt, validar inputs y outputs.
    """
    name: str = "base"

    @abstractmethod
    def get_prompt(self, query: str, context: str | None = None) -> str:
        ...

    def validate_result(self, result: dict) -> None:
        """
        Lanza excepciones si el resultado no cumple las reglas.
        """
        if 'error' in result:
            raise ValueError(f"Pipeline {self.name} error: {result['error']}")