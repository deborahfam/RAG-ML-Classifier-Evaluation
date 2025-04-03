import streamlit as st
import os, dotenv
from services.db.mongodb import MongoDBService
from services.text_processor import TextProcessor
from services.crawler import CrawlerService
from services.embeddings import EmbeddingService
from services.doc_processor import DocumentProcessorService

dotenv.load_dotenv()
st.set_page_config(page_title="RAG System - Crawler & Document Processor", page_icon="🤖", layout="wide")

# Initialize services
embedding_model = EmbeddingService()
db_service = MongoDBService()
text_processor = TextProcessor(embedding_model)
crawler = CrawlerService(db_service, text_processor)
doc_processor = DocumentProcessorService(embedding_model)

def process_pdf(uploaded_file):
    """Process the uploaded PDF file."""
    try:
        with st.spinner(f"Processing PDF: {uploaded_file.name}"):
            doc_processor.process_and_save(uploaded_file)
        st.success(f"PDF processed successfully: {uploaded_file.name}")
    except Exception as e:
        st.error(f"Error processing PDF: {str(e)}")

def process_web_crawling(url, max_depth):
    """Process web crawling for the given URL."""
    try:
        with st.spinner(f"Crawling URL: {url}"):
            crawler.crawl(url, max_depth)
        st.success(f"Web crawling completed for: {url}")
    except Exception as e:
        st.error(f"Error during web crawling: {str(e)}")

def main():
    st.title("🤖 RAG System - Crawler & Document Processor")
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Select Service", ["Document Processor", "Web Crawler"])
    
    if page == "Document Processor":
        st.header("📚 Document Processor")
        st.write("Upload PDF documents to process and store in the database.")
        
        uploaded_files = st.file_uploader(
            "Choose PDF files", 
            type=["pdf"], 
            accept_multiple_files=True
        )
        
        if uploaded_files:
            if st.button("Process Documents"):
                for uploaded_file in uploaded_files:
                    process_pdf(uploaded_file)
    
    elif page == "Web Crawler":
        st.header("🌐 Web Crawler")
        st.write("Enter URLs to crawl and store in the database.")
        
        # Input method selection
        input_method = st.selectbox(
            "Select input method",
            ["Single URL", "Multiple URLs"]
        )
        
        urls = []
        if input_method == "Single URL":
            url = st.text_input("Enter URL")
            if url:
                urls.append(url)
        else:
            urls_input = st.text_area("Enter multiple URLs (one per line)")
            if urls_input:
                urls = [url.strip() for url in urls_input.splitlines() if url.strip()]
        
        max_depth = st.slider("Max Crawling Depth", 1, 5, 2)
        
        if st.button("Start Crawling"):
            if urls:
                for url in urls:
                    process_web_crawling(url, max_depth)
            else:
                st.error("Please enter at least one valid URL.")

if __name__ == "__main__":
    main()
