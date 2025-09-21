"""
Database/Storage layer for managing chat sessions, messages, and documents.
This is a simple in-memory implementation that can be replaced with a proper database.
Future implementations, experiment with MongoDB
"""

import uuid
from typing import Dict, List, Optional
from datetime import datetime
from models import ChatMessage, DocumentInfo
from logging_config import logger
import os
from pathlib import Path
from config import settings


class InMemoryDatabase:
    """Simple in-memory database for storing chat sessions and documents"""
    
    def __init__(self):
        self.chat_sessions: Dict[str, List[ChatMessage]] = {}
        self.documents: Dict[str, DocumentInfo] = {}
        self._initialize_documents()
    
    def _initialize_documents(self):
        """Initialize documents from the data directory"""
        logger.info("Initializing documents from data directory")
        
        data_path = Path(settings.data_directory)
        if not data_path.exists():
            logger.warning(f"Data directory {settings.data_directory} does not exist")
            return
        
        for file_path in data_path.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in settings.allowed_file_types_list:
                doc_id = f"doc-{uuid.uuid4().hex[:8]}"
                doc_type = file_path.suffix.upper().replace(".", "")
                
                document = DocumentInfo(
                    id=doc_id,
                    name=file_path.name,
                    type=doc_type
                )
                
                self.documents[doc_id] = document
                logger.info(f"Added document: {document.name} (ID: {doc_id})")
    
    def get_documents(self, chat_id: str) -> List[DocumentInfo]:
        """Get all available documents for a chat session"""
        logger.info(f"Retrieving documents for chat session: {chat_id}")
        return list(self.documents.values())
    
    def create_chat_session(self, chat_id: str) -> bool:
        """Create a new chat session"""
        if chat_id not in self.chat_sessions:
            self.chat_sessions[chat_id] = []
            logger.info(f"Created new chat session: {chat_id}")
            return True
        return False
    
    def add_message(self, chat_id: str, message: ChatMessage) -> bool:
        """Add a message to a chat session"""
        if chat_id not in self.chat_sessions:
            self.create_chat_session(chat_id)
        
        self.chat_sessions[chat_id].append(message)
        logger.info(f"Added message to chat {chat_id}: {message.role} - {message.content[:50]}...")
        return True
    
    def get_chat_history(self, chat_id: str) -> List[ChatMessage]:
        """Get chat history for a session"""
        logger.info(f"Retrieving chat history for session: {chat_id}")
        return self.chat_sessions.get(chat_id, [])
    
    def delete_chat_session(self, chat_id: str) -> bool:
        """Delete a chat session"""
        if chat_id in self.chat_sessions:
            del self.chat_sessions[chat_id]
            logger.info(f"Deleted chat session: {chat_id}")
            return True
        logger.warning(f"Attempted to delete non-existent chat session: {chat_id}")
        return False
    
    def chat_session_exists(self, chat_id: str) -> bool:
        """Check if a chat session exists"""
        return chat_id in self.chat_sessions
    
    def get_all_chat_sessions(self) -> List[str]:
        """Get all chat session IDs"""
        return list(self.chat_sessions.keys())
    
    def get_chat_sessions_with_metadata(self) -> List[dict]:
        """Get all chat sessions with metadata"""        
        sessions = []
        for chat_id, messages in self.chat_sessions.items():
            if not messages:
                continue
                
            # Get first user message for preview
            first_user_message = None
            for msg in messages:
                if msg.role == "user":
                    first_user_message = msg.content[:100] + "..." if len(msg.content) > 100 else msg.content
                    break
            
            # Get last activity timestamp
            last_activity = messages[-1].timestamp if messages else datetime.utcnow().isoformat() + "Z"
            
            session_info = {
                "chatId": chat_id,
                "messageCount": len(messages),
                "lastActivity": last_activity,
                "firstMessage": first_user_message
            }
            sessions.append(session_info)
        
        # Sort by last activity (most recent first)
        sessions.sort(key=lambda x: x["lastActivity"], reverse=True)
        return sessions


# Global database instance
db = InMemoryDatabase()
