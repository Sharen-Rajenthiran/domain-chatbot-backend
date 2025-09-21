from services.helper import load_pdf_file, text_split, download_hugging_face_embeddings
from langchain_core.vectorstores import InMemoryVectorStore
from config import settings
from logging_config import logger

def create_in_memory_vector_store():
    """
    Create an in-memory vector store from documents in the data directory.
    
    Returns:
        InMemoryVectorStore instance with embedded documents
    """
    logger.info("Creating in-memory vector store")
    
    try:
        # Load documents from data directory
        extracted_data = load_pdf_file(data_directory=settings.data_directory)
        
        if not extracted_data:
            logger.warning("No documents found to create vector store")
            # Create empty vector store
            embeddings = download_hugging_face_embeddings()
            return InMemoryVectorStore(embeddings)
        
        # Split documents into chunks
        chunks = text_split(extracted_data)
        
        if not chunks:
            logger.warning("No text chunks created from documents")
            embeddings = download_hugging_face_embeddings()
            return InMemoryVectorStore(embeddings)
        
        # Initialize embeddings
        embeddings = download_hugging_face_embeddings()
        
        # Create vector store
        vector_store = InMemoryVectorStore.from_documents(chunks, embedding=embeddings)
        
        logger.info(f"Successfully created vector store with {len(chunks)} document chunks")
        return vector_store
        
    except Exception as e:
        logger.error(f"Error creating vector store: {str(e)}", exc_info=True)
        # Return empty vector store as fallback
        try:
            embeddings = download_hugging_face_embeddings()
            return InMemoryVectorStore(embeddings)
        except Exception as fallback_error:
            logger.error(f"Failed to create fallback vector store: {str(fallback_error)}")
            raise