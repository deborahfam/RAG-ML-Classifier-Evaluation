from typing import List, Tuple
from scrapping.services.db.models import DocumentMetadataModel
from services.embeddings import EmbeddingService
from services.main import MainService
import os
import dotenv

dotenv.load_dotenv()

# Environment Variables
LLM_MODEL = os.getenv("LLM_MODEL")

from prompts import (
    GENERATE_QUESTIONS,
    GENERATE_IDEAS,
    GENERATE_SUMMARIZE
)

class DocumentMetadataGenerator:
    def __init__(self, embedding_model: EmbeddingService) -> None:
        self.embedding_model = embedding_model
        self.handler = MainService(embedding_model=embedding_model)
        self.model = LLM_MODEL

    def process_questions(self, chunk: str) -> Tuple[List[str], List[List[float]]]:
        """Generate questions and their embeddings."""
        questions = self.handler.generate_request_by_prompt(
            PROMPT=GENERATE_QUESTIONS, model=self.model, query=chunk
        )
        questions_embedded = self.embedding_model.embed_query(questions)
        return questions, questions_embedded

    def process_summary(self, text: str) -> Tuple[str, List[float]]:
        """Generate summary and its embedding."""
        summary = self.handler.generate_request_by_prompt(
            PROMPT=GENERATE_SUMMARIZE, model=self.model, query=text
        )
        summary_embedded = self.embedding_model.embed_query(summary)
        return summary, summary_embedded

    def process_principal_ideas(self, text: str) -> Tuple[List[str], List[List[float]]]:
        """Generate principal ideas and their embeddings."""
        principal_ideas = self.handler.generate_request_by_prompt(
            PROMPT=GENERATE_IDEAS, model=self.model, query=text
        )
        principal_ideas_embedded = self.embedding_model.embed_query(principal_ideas)
        return principal_ideas, principal_ideas_embedded

    def process_metadata(self, chunk):
        questions, questions_embedded = self.process_questions(chunk["text"])
        summary, summary_embedded = self.process_summary(chunk["text"])
        principal_ideas, principal_ideas_embedded = self.process_principal_ideas(
            chunk["text"]
        )
        metadata = DocumentMetadataModel(
            questions=questions,
            questions_embedded=questions_embedded,
            principal_ideas=principal_ideas,
            principal_ideas_embedded=principal_ideas_embedded,
            summarize=summary,
            summarize_embedded=summary_embedded,
        )
        metadata_id = self.db_handler.insert_one(
            "document_metadata_table", metadata.model_dump(by_alias=True)
        )
        return metadata_id

    def generate_all_metadata(self, text: str) -> dict:
        """Generate all metadata types for a given text."""
        questions, questions_embedded = self.generate_questions(text)
        summary, summary_embedded = self.generate_summary(text)
        principal_ideas, principal_ideas_embedded = self.generate_principal_ideas(text)

        return {
            "questions": questions,
            "questions_embedded": questions_embedded,
            "principal_ideas": principal_ideas,
            "principal_ideas_embedded": principal_ideas_embedded,
            "summary": summary,
            "summary_embedded": summary_embedded
        }
