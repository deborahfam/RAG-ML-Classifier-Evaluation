from pydantic import BaseModel

class ClassificationModel(BaseModel):
    reasoning: str
    classification: str