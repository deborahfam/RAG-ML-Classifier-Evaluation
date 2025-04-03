import streamlit as st
import os
from scrapping.services.doc_processor import DocumentProcessorService
from scrapping.services.embeddings import EmbeddingService
import tempfile

# Initialize the services
embedding_service = EmbeddingService()
doc_processor = DocumentProcessorService(embedding_service)

def process_pdf(uploaded_file):
    """Process the uploaded PDF file."""
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_file_path = tmp_file.name
    
    try:
        with open(tmp_file_path, 'rb') as file:
            doc_processor.process_and_save(file)
        st.success("PDF processed successfully!")
    except Exception as e:
        st.error(f"Error processing PDF: {str(e)}")
    finally:
        os.unlink(tmp_file_path)

def main():
    st.title("PDF Processing App")
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Upload PDF", "View Processed Documents"])
    
    if page == "Upload PDF":
        st.header("Upload and Process PDF")
        uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
        
        if uploaded_file is not None:
            if st.button("Process PDF"):
                with st.spinner("Processing PDF..."):
                    process_pdf(uploaded_file)
    
    elif page == "View Processed Documents":
        st.header("Processed Documents")
        # TODO: Add functionality to view processed documents
        st.info("This feature will be implemented soon!")

if __name__ == "__main__":
    main() 