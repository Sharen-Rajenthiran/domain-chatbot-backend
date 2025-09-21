"""
Documents API endpoints for the Domain Chatbot backend.
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List
from models import DocumentsResponse, DocumentInfo
from services.database import db
from logging_config import logger

router = APIRouter()


@router.get("/docs", response_model=DocumentsResponse)
async def get_documents(chatId: str = Query(..., description="The ID of the chat session")):
    """
    Get all available documents for a chat session.
    
    Args:
        chatId: The ID of the chat session
        
    Returns:
        DocumentsResponse containing list of available documents
    """
    logger.info(f"Documents endpoint accessed for chat session: {chatId}")
    
    try:
        # Validate chat_id format (basic validation)
        if not chatId or len(chatId.strip()) == 0:
            logger.warning("Empty or invalid chatId provided")
            raise HTTPException(status_code=400, detail="chatId cannot be empty")
        
        # Get documents from database
        documents = db.get_documents(chatId)
        
        logger.info(f"Retrieved {len(documents)} documents for chat session: {chatId}")
        
        return DocumentsResponse(docs=documents)
        
    except HTTPException as e:
        logger.error(f"HTTP exception in documents endpoint: {e.detail}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in documents endpoint: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
