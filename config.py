import os
from typing import Optional, List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application configuration settings"""

    # Hugging Face Configuration
    huggingface_token: Optional[str] = os.environ.get("HUGGINGFACE_TOKEN")
    huggingface_embeddings_model: Optional[str] = os.environ.get("HUGGINGFACE_EMBEDDINGS_MODEL")
    huggingface_chat_model: Optional[str] = os.environ.get("HUGGINGFACE_CHAT_MODEL")

    # Server Configuration
    host: str = "localhost"
    port: int = 8001
    debug: bool = False
    
    # API Configuration
    api_prefix: str = "/api"
    api_version: str = "v1"
    
    # Document Configuration
    data_directory: str = "data"
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    allowed_file_types: str = ".pdf,.docx,.txt"  # Comma-separated string
    
    # Text Processing Configuration
    chunk_size: int = 500
    chunk_overlap: int = 20
    max_tokens: int = 150
    
    # Logging Configuration
    log_level: str = "INFO"
    log_file: str = "domain-chatbot-backend.log"
    
    # CORS Configuration
    allowed_origins: str = "http://localhost:3000,http://127.0.0.1:3000"  # Comma-separated string

    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"  # Ignore extra fields

    def validate_huggingface_config(self) -> bool:
        """Validate that Hugging Face configuration is complete."""
        return bool(self.huggingface_token and self.huggingface_embeddings_model and self.huggingface_chat_model)
    
    @property
    def allowed_file_types_list(self) -> List[str]:
        """Convert comma-separated allowed_file_types to a list."""
        return [ext.strip() for ext in self.allowed_file_types.split(",")]
    
    @property
    def allowed_origins_list(self) -> List[str]:
        """Convert comma-separated allowed_origins to a list if it's a string."""
        if isinstance(self.allowed_origins, str):
            return [origin.strip() for origin in self.allowed_origins.split(",")]
        return self.allowed_origins
    
settings = Settings()

# Validate configuration on startup
if not settings.validate_huggingface_config():
    print("Warning: Hugging Face configuration is incomplete.")
    print("Please set the following environment variables:")
    print("- Hugging Face token")
    print("The server will start but chat functionality may not work.")