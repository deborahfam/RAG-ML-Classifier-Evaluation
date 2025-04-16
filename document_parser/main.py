from services.pipeline import PDFProcessingPipeline

if __name__ == "__main__":
    pdf_dir = "pdfs"
    pipeline = PDFProcessingPipeline(pdf_dir)
    pipeline.process_pdfs()
