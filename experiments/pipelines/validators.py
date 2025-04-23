import re
from typing import Any, Dict, List

class PromptValidator:
    """
    Validaciones sobre las plantillas de prompt.
    """
    @staticmethod
    def check_placeholders(template: str, required: List[str]) -> List[str]:
        missing = []
        for p in required:
            if f"{{{p}}}" not in template:
                missing.append(p)
        return missing

class ResultValidator:
    """
    Validaciones sobre los resultados retornados por los pipelines.
    """
    @staticmethod
    def is_json_serializable(obj: Any) -> bool:
        try:
            import json
            json.dumps(obj)
            return True
        except Exception:
            return False