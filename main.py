from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from api.chat import router as chat_router
from logging_config import logger

# Create FastAPI application
app = FastAPI(
    title="Domain Chatbot API",
    description="AI-powered chatbot for domain specific",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

logger.info("Starting Domain Chatbot API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat_router, prefix="/api/v1", tags=["chat"])


@app.get("/")
async def root():
    """Root endpoint."""
    logger.info("Root endpoint accessed")
    return {
        "message": "Welcome to Domain Chatbot API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    logger.info("Health check endpoint accessed")
    return {"status": "healthy", "message": "Service is running"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )