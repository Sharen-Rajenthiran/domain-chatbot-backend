"""
Chat API endpoints for the Domain Chatbot backend.
"""

import uuid
from datetime import datetime
from fastapi import APIRouter, HTTPException, Path
from typing import List
from models import (
    ChatRequest, 
    ChatResponse, 
    ChatHistoryResponse, 
    DeleteChatResponse,
    ChatListResponse,
    ChatSession,
    ChatMessage,
    SourceDocument
)
from services.database import db
from services import store
from services import model
from logging_config import logger

# Initialize the vector store and QA chain
vector_store = store.create_in_memory_vector_store()
retriever = vector_store.as_retriever()
qa_chain = model.model(retriever=retriever)

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Process a chat message and return AI response.
    
    Args:
        request: Chat request containing chatId, message, and optional userId
        
    Returns:
        ChatResponse with AI assistant's response and metadata
    """
    try:
        # Validate request
        if not request.message.strip():
            logger.warning("Empty message received")
            raise HTTPException(status_code=400, detail="Message cannot be empty")
        
        # Auto-generate chatId if not provided
        chat_id = request.chatId
        if not chat_id or not chat_id.strip() or chat_id == "string":
            chat_id = f"chat-{uuid.uuid4().hex[:8]}"
            logger.info(f"Auto-generated chatId: {chat_id}")
        
        logger.info(f"Chat request received for session {chat_id}: {request.message[:100]}...")
        
        # Auto-generate userId if not provided
        user_id = request.userId
        if not user_id or not user_id.strip() or user_id == "string":
            user_id = f"user-{uuid.uuid4().hex[:8]}"
            logger.info(f"Auto-generated userId: {user_id}")
        
        # Ensure chat session exists
        if not db.chat_session_exists(chat_id):
            db.create_chat_session(chat_id)
            logger.info(f"Created new chat session: {chat_id}")
        
        # Get conversation history
        conversation_history = db.get_chat_history(chat_id)
        logger.info(f"Processing chat with {len(conversation_history)} previous messages")
        
        # Convert to format expected by the model
        history_for_model = [
            {"role": msg.role, "content": msg.content} 
            for msg in conversation_history[-10:]  # Limit to last 10 messages
        ]
        
        # Generate response using the QA chain
        try:
            # Test numpy availability first
            # Had problems with Numpy package
            try:
                import numpy as np
                logger.info(f"NumPy version: {np.__version__}")
            except ImportError as np_error:
                logger.error(f"NumPy import error: {np_error}")
                raise Exception("NumPy is not properly installed")
            
            response_text = qa_chain.invoke({
                "query": request.message
            })
            
            # Extract the answer from the response
            if isinstance(response_text, dict) and "result" in response_text:
                ai_response = response_text["result"]
            else:
                ai_response = str(response_text)
                
        except Exception as model_error:
            logger.error(f"Model error: {str(model_error)}", exc_info=True)
            
            # Provide more specific error messages
            if "Numpy is not available" in str(model_error):
                ai_response = "I'm experiencing a technical issue with the numerical computing library. Please ensure NumPy is properly installed."
            elif "CUDA" in str(model_error) or "GPU" in str(model_error):
                ai_response = "I'm having GPU-related issues. The system will try to use CPU instead."
            else:
                ai_response = "I apologize, but I'm having trouble processing your request right now. Please try again later."
        
        # Generate unique message IDs
        user_message_id = f"msg-{uuid.uuid4().hex[:8]}"
        assistant_message_id = f"msg-{uuid.uuid4().hex[:8]}"
        current_timestamp = datetime.utcnow().isoformat() + "Z"
        
        # Store user message
        user_message = ChatMessage(
            id=user_message_id,
            role="user",
            content=request.message,
            timestamp=current_timestamp
        )
        db.add_message(chat_id, user_message)
        
        # Store assistant message
        assistant_message = ChatMessage(
            id=assistant_message_id,
            role="assistant",
            content=ai_response,
            timestamp=current_timestamp
        )
        db.add_message(chat_id, assistant_message)
        
        # Get source documents, simplified
        documents = db.get_documents(chat_id)
        sources = [
            SourceDocument(
                docId=doc.id,
                docName=doc.name,
                relevantSection=None
            )
            for doc in documents[:3]  # Limit to first 3 documents
        ] if documents else None
        
        logger.info(f"Chat response generated successfully for session {chat_id}")
        
        return ChatResponse(
            response=ai_response,
            messageId=assistant_message_id,
            chatId=chat_id,
            userId=user_id,
            timestamp=current_timestamp,
            sources=sources
        )
        
    except HTTPException as e:
        logger.error(f"HTTP exception in chat endpoint: {e.detail}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in chat endpoint: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/chats/{chatId}/messages", response_model=ChatHistoryResponse)
async def get_chat_history(
    chatId: str = Path(..., description="The ID of the chat session")
):
    """
    Get chat history for a specific chat session.
    
    Args:
        chatId: The ID of the chat session
        
    Returns:
        ChatHistoryResponse containing list of messages
    """
    logger.info(f"Chat history requested for session: {chatId}")
    
    try:
        # Validate chatId
        if not chatId.strip():
            logger.warning("Empty chatId provided")
            raise HTTPException(status_code=400, detail="chatId cannot be empty")
        
        # Get chat history
        messages = db.get_chat_history(chatId)
        
        logger.info(f"Retrieved {len(messages)} messages for chat session: {chatId}")
        
        return ChatHistoryResponse(messages=messages)
        
    except HTTPException as e:
        logger.error(f"HTTP exception in chat history endpoint: {e.detail}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in chat history endpoint: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/chats", response_model=ChatListResponse)
async def list_chats():
    """
    Get a list of all chat sessions with metadata.
    
    Returns:
        ChatListResponse containing list of chat sessions with metadata
    """
    logger.info("List chats endpoint accessed")
    
    try:
        # Get all chat sessions with metadata
        sessions_data = db.get_chat_sessions_with_metadata()
        
        # Convert to ChatSession models
        chat_sessions = [
            ChatSession(
                chatId=session["chatId"],
                messageCount=session["messageCount"],
                lastActivity=session["lastActivity"],
                firstMessage=session["firstMessage"]
            )
            for session in sessions_data
        ]
        
        logger.info(f"Retrieved {len(chat_sessions)} chat sessions")
        
        return ChatListResponse(chats=chat_sessions)
        
    except Exception as e:
        logger.error(f"Unexpected error in list chats endpoint: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.delete("/chats/{chatId}", response_model=DeleteChatResponse)
async def delete_chat(
    chatId: str = Path(..., description="The ID of the chat session to delete")
):
    """
    Delete a chat session and all its messages.
    
    Args:
        chatId: The ID of the chat session to delete
        
    Returns:
        DeleteChatResponse indicating success or failure
    """
    logger.info(f"Delete chat requested for session: {chatId}")
    
    try:
        # Validate chatId
        if not chatId.strip():
            logger.warning("Empty chatId provided")
            raise HTTPException(status_code=400, detail="chatId cannot be empty")
        
        # Attempt to delete the chat session
        success = db.delete_chat_session(chatId)
        
        if success:
            logger.info(f"Successfully deleted chat session: {chatId}")
            return DeleteChatResponse(
                success=True,
                message=f"Chat session {chatId} has been successfully deleted"
            )
        else:
            logger.warning(f"Chat session not found: {chatId}")
            raise HTTPException(
                status_code=404, 
                detail=f"Chat session {chatId} not found"
            )
        
    except HTTPException as e:
        logger.error(f"HTTP exception in delete chat endpoint: {e.detail}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in delete chat endpoint: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
