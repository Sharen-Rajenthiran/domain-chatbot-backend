from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from config import settings
from api.chats import router as chats_router
from api.documents import router as documents_router
from logging_config import logger
from models import HealthResponse
import uvicorn


app = FastAPI(
    title="Domain Chatbot API",
    description="AI-powered chatbot for domain-specific document Q&A",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers with proper prefixes
app.include_router(
    chats_router, 
    prefix=f"{settings.api_prefix}", 
    tags=["chats"]
)
app.include_router(
    documents_router, 
    prefix=f"{settings.api_prefix}", 
    tags=["documents"]
)


@app.get("/")
async def root():
    """Root endpoint."""
    logger.info("Root endpoint accessed")
    return {
        "message": "Welcome to Domain Chatbot API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health", response_model=HealthResponse)
async def health():
    """Health check endpoint."""
    logger.info("Health check endpoint accessed")
    return HealthResponse(
        status="healthy", 
        message="Service is running",
        timestamp=datetime.utcnow().isoformat() + "Z"
    )


if __name__ == "__main__":
    logger.info("Starting Domain Chatbot API at main")
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )