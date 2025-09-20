import os
from typing import Optional, List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application configuration settings"""

    huggingface_token: Optional[str] = os.environ.get("HUGGINGFACE_TOKEN")
    huggingface_embeddings_model: Optional[str] = os.environ.get("HUGGINGFACE__EMBEDDINGS_MODEL")
    huggingface_chat_model: Optional[str] = os.environ.get("HUGGINFACE_CHAT_MODEL")

    host: str = "localhost"
    port: int = 8001
    debug: bool = False

    allowed_origins: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]

    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"  # Ignore extra fields

    def validate_huggingface_config(self) -> bool:
        """Validate that Azure OpenAI configuration is complete."""
        return bool(self.huggingface_token)
    
settings = Settings()

# Validate configuration on startup
if not settings.validate_huggingface_config():
    print("Warning: Hugging Face configuration is incomplete.")
    print("Please set the following environment variables:")
    print("- Hugging Face token")
    print("The server will start but chat functionality may not work.")