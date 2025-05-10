from pydantic import BaseModel
import enum
class CLASSIFICATION(enum):
    CLASSIFICATION: 1
    REGRESSION: 2
    CLUSTERING: 3

class ClassificationModel(BaseModel):
    reasoning: str
    classification: CLASSIFICATION