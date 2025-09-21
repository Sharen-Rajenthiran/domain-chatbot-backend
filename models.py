from typing import List, Optional, Literal
from pydantic import BaseModel, Field
from datetime import datetime

# Document Models
class DocumentInfo(BaseModel):
    """Model for document information"""
    id: str = Field(..., description="Unique document identifier")
    name: str = Field(..., description="Document name")
    type: str = Field(..., description="Document type (PDF, DOCX, etc.)")

class DocumentsResponse(BaseModel):
    """Response model for documents endpoint"""
    docs: List[DocumentInfo] = Field(..., description="List of available documents")

# Chat Models
class ChatMessage(BaseModel):
    """Model for individual chat messages"""
    id: str = Field(..., description="Unique message identifier")
    role: Literal["user", "assistant"] = Field(..., description="Message role")
    content: str = Field(..., description="Message content")
    timestamp: str = Field(..., description="ISO timestamp")

class SourceDocument(BaseModel):
    """Model for source document references"""
    docId: str = Field(..., description="Document ID")
    docName: str = Field(..., description="Document name")
    relevantSection: Optional[str] = Field(None, description="Relevant section of the document")

class ChatRequest(BaseModel):
    """Request model for chat endpoint"""
    chatId: Optional[str] = Field(None, description="Chat session ID (auto-generated if not provided)")
    message: str = Field(..., description="User's message")
    userId: Optional[str] = Field(None, description="Optional user identifier (auto-generated if not provided)")

class ChatResponse(BaseModel):
    """Response model for chat endpoint"""
    response: str = Field(..., description="AI assistant's response")
    messageId: str = Field(..., description="Unique message identifier")
    chatId: str = Field(..., description="Chat session ID used")
    userId: Optional[str] = Field(None, description="User ID used")
    timestamp: str = Field(..., description="ISO timestamp")
    sources: Optional[List[SourceDocument]] = Field(None, description="Source documents used")

class ChatHistoryResponse(BaseModel):
    """Response model for chat history endpoint"""
    messages: List[ChatMessage] = Field(..., description="List of chat messages")

class DeleteChatResponse(BaseModel):
    """Response model for delete chat endpoint"""
    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Status message")

class ChatSession(BaseModel):
    """Model for chat session information"""
    chatId: str = Field(..., description="Chat session ID")
    messageCount: int = Field(..., description="Number of messages in the chat")
    lastActivity: str = Field(..., description="Last activity timestamp")
    firstMessage: Optional[str] = Field(None, description="Preview of the first user message")

class ChatListResponse(BaseModel):
    """Response model for list all chats endpoint"""
    chats: List[ChatSession] = Field(..., description="List of chat sessions")

# Health and Status Models
class HealthResponse(BaseModel):
    """Model for health check responses"""
    status: str = Field(..., description="Service status")
    message: str = Field(..., description="Status message")
    timestamp: str = Field(..., description="Current timestamp")

class ErrorResponse(BaseModel):
    """Model for error responses"""
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    timestamp: str = Field(..., description="Error timestamp")