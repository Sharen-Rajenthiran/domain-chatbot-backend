from fastapi import APIRouter, HTTPException
from models import ChatResponse, ChatRequest
from services import store
from services import model
from logging_config import logger


vector_store = store.create_in_memory_vector_store()
retriever = vector_store.as_retriever()
qa_chain = model(retriever=retriever)

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat endpoint for interacting with the AI bot.
    
    Args:
        request: Chat request containing message and optional conversation history
        
    Returns:
        Chat response from the AI assistant
    """
    logger.info(f"Chat request received: {request.message[:100]}...")
    
    try:
        if not request.message.strip():
            logger.warning("Empty message received")
            raise HTTPException(status_code=400, detail="Message cannot be empty")
        
        # Log conversation history length
        history_length = len(request.conversation_history) if request.conversation_history else 0
        logger.info(f"Processing chat with {history_length} previous messages")
        
        # Get response from Azure OpenAI
        response =qa_chain(
            user_message=request.message,
            conversation_history=request.conversation_history
        )
        
        logger.info(f"Chat response generated successfully: {response[:100]}...")
        
        return ChatResponse(
            response=response,
            conversation_id=None  # Could be implemented for session management
        )
        
    except HTTPException as e:
        logger.error(f"HTTP exception in chat endpoint: {e.detail}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in chat endpoint: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")