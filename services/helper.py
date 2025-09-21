from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from config import settings
from logging_config import logger
import os
from pathlib import Path

def load_pdf_file(data_directory: str = None):
    """
    Load PDF files from the specified directory.
    
    Args:
        data_directory: Directory path containing PDF files
        
    Returns:
        List of loaded documents
    """
    if data_directory is None:
        data_directory = settings.data_directory
    
    logger.info(f"Loading PDF files from directory: {data_directory}")
    
    # Ensure directory exists
    if not os.path.exists(data_directory):
        logger.error(f"Data directory does not exist: {data_directory}")
        return []
    
    try:
        loader = DirectoryLoader(
            data_directory,
            glob="*.pdf",
            loader_cls=PyPDFLoader
        )
        
        documents = loader.load()
        logger.info(f"Successfully loaded {len(documents)} PDF documents")
        return documents
        
    except Exception as e:
        logger.error(f"Error loading PDF files: {str(e)}", exc_info=True)
        return []

def text_split(extracted_data):
    """
    Split documents into smaller chunks for processing.
    
    Args:
        extracted_data: List of documents to split
        
    Returns:
        List of text chunks
    """
    logger.info(f"Splitting {len(extracted_data)} documents into chunks")
    
    try:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.chunk_size, 
            chunk_overlap=settings.chunk_overlap
        )
        text_chunks = text_splitter.split_documents(extracted_data)
        
        logger.info(f"Successfully created {len(text_chunks)} text chunks")
        return text_chunks
        
    except Exception as e:
        logger.error(f"Error splitting text: {str(e)}", exc_info=True)
        return []

def download_hugging_face_embeddings():
    """
    Initialize Hugging Face embeddings model.
    
    Returns:
        HuggingFaceEmbeddings instance
    """
    logger.info(f"Initializing Hugging Face embeddings model: {settings.huggingface_embeddings_model}")
    
    try:
        embeddings = HuggingFaceEmbeddings(
            model_name=settings.huggingface_embeddings_model
        )
        logger.info("Successfully initialized embeddings model")
        return embeddings
        
    except Exception as e:
        logger.error(f"Error initializing embeddings model: {str(e)}", exc_info=True)
        raise