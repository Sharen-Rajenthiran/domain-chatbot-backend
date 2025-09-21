from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline
from langchain_core.prompts import PromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from transformers import pipeline
from langchain.chains import RetrievalQA
from huggingface_hub import login
from dotenv import load_dotenv
from config import settings
from services.system_prompt import system_prompt
from logging_config import logger

# Login to Hugging Face if token is available
if settings.huggingface_token:
    try:
        login(settings.huggingface_token)
        logger.info("Successfully logged in to Hugging Face")
    except Exception as e:
        logger.error(f"Failed to login to Hugging Face: {str(e)}")

def docs_to_text(docs):
    """
    Convert a list of documents to a single text string.
    
    Args:
        docs: List of document objects
        
    Returns:
        Combined text string
    """
    return "\n\n".join([doc.page_content for doc in docs])

def model(retriever):
    """
    Create a QA chain model using Hugging Face pipeline and retriever.
    
    Args:
        retriever: Document retriever instance
        
    Returns:
        RetrievalQA chain instance
    """
    logger.info(f"Initializing model with Hugging Face chat model: {settings.huggingface_chat_model}")
    
    try:
        # Create Hugging Face pipeline
        pipe = pipeline(
            "text2text-generation", 
            model=settings.huggingface_chat_model, 
            max_new_tokens=settings.max_tokens
        )
        llm = HuggingFacePipeline(pipeline=pipe)
        
        # Create prompt template
        PROMPT = PromptTemplate(
            template=system_prompt, 
            input_variables=["context", "question"]
        )
        
        # Create document chain
        document_chain = create_stuff_documents_chain(llm=llm, prompt=PROMPT)
        
        # Create QA chain
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=retriever,
            chain_type="stuff",
            chain_type_kwargs={"prompt": PROMPT}
        )
        
        logger.info("Successfully initialized QA chain model")
        return qa_chain
        
    except Exception as e:
        logger.error(f"Error initializing model: {str(e)}", exc_info=True)
        raise