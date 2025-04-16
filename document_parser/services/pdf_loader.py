import os
from typing import List, Tuple
from pypdf import PdfReader
from pathlib import Path
import pymupdf4llm

class PDFLoader:
    def __init__(self, pdf_dir: str, backend: str = "fitz"):
        self.pdf_dir = Path(pdf_dir)
        self.backend = backend

    def get_pdf_files(self):
        return list(self.pdf_dir.glob("*.pdf"))

    def extract_pages(self, pdf_path: str):
        if self.backend == "pymupdf4llm":
            return self._extract_with_pymupdf4llm(pdf_path)
        elif self.backend == "pypdf":
            return self._extract_with_pypdf(pdf_path)
        else:
            raise ValueError(f"Unsupported backend: {self.backend}")

    def _extract_with_pymupdf4llm(self, pdf_path: str):
        md_pages = pymupdf4llm.to_markdown(pdf_path, page_chunks=True)
        return [(i + 1, page_md['text']) for i, page_md in enumerate(md_pages)]

    def _extract_with_pypdf(self, pdf_path: str):
        with open(pdf_path, "rb") as f:
            reader = PdfReader(f)
            return [(i + 1, page.extract_text() or "") for i, page in enumerate(reader.pages)]
