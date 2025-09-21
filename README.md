# Domain Chatbot Backend

A FastAPI backend for a domain-specific chatbot that uses Hugging Face models to answer questions based on ingested documents.

## Features

- **Document Ingestion**: Automatically loads and processes PDF documents from the data directory using LangChain
- **Vector Search**: Uses Hugging Face embeddings for semantic document search
- **Chat Interface**: RESTful API endpoints for chat interactions
- **Session Management**: Maintains chat history and session state
- **Comprehensive Logging**: Extensive logging with file output
- **Production Ready**: Structured codebase following FastAPI best practices (to the best of my knowledge)

## API Endpoints

### Documents
- `GET /api/docs?chatId={chatId}` - Get available documents for a chat session (show what documents are ingested)

### Chat
- `POST /api/chat` - Send a message and get AI response
- `GET /api/chats` - List all chat sessions with metadata
- `GET /api/chats/{chatId}/messages` - Get chat history
- `DELETE /api/chats/{chatId}` - Delete a chat session

### Health
- `GET /health` - Health check endpoint
- `GET /` - Root endpoint with API information

## Project Structure

```
domain-chatbot-backend/
├── api/                    # API route handlers
│   ├── chats.py           # Chat-related endpoints
│   └── documents.py       # Document-related endpoints
├── services/              # Business logic services
│   ├── database.py        # In-memory database for sessions
│   ├── helper.py          # Document processing utilities
│   ├── model.py           # Hugging Face model setup
│   ├── store.py           # Vector store management
│   └── system_prompt.py   # AI system prompt
├── data/                  # Document storage directory
├── config.py              # Application configuration
├── logging_config.py      # Logging setup
├── main.py               # FastAPI application entry point
├── models.py             # Pydantic data models
└── requirements.txt      # Python dependencies
```

## Setup

### 1. Environment Variables

Create a `.env` file in the project root with the following variables:

```env
HUGGINGFACE_TOKEN=your_huggingface_token_here
HUGGINGFACE_EMBEDDINGS_MODEL=choose_your_huggingface_embeddings_model
HUGGINGFACE_CHAT_MODEL=choose_your_huggingface_chat_model
```
You can refer to `.env.example` for the example env

### 2. Install Dependencies

```bash
python -m venv your_venv_name
your_venv_name/Scripts/Activate
```

```bash
pip install -r requirements.txt
```

### 3. Add Documents

Place your PDF documents in the `data/` directory. The system will automatically:
- Load all PDF files from this directory
- Process them into text chunks
- Create embeddings for semantic search

### 4. Run the Application

```bash
python main.py
```

The API will be available at:
- **API**: http://localhost:8001
- **Documentation**: http://localhost:8001/docs
- **ReDoc**: http://localhost:8001/redoc

## Configuration

The application can be configured through environment variables or by modifying `config.py`:

- `HOST`: Server host (default: localhost)
- `PORT`: Server port (default: 8001)
- `DEBUG`: Debug mode (default: False)
- `DATA_DIRECTORY`: Document storage directory (default: data)
- `CHUNK_SIZE`: Text chunk size for processing (default: 500)
- `CHUNK_OVERLAP`: Overlap between chunks (default: 20)
- `MAX_TOKENS`: Maximum tokens for model response (default: 150)
- `LOG_LEVEL`: Logging level (default: INFO)
- `LOG_FILE`: Log file name (default: domain-chatbot-backend.log)

## API Usage Examples

### Get Documents
```bash
curl "http://localhost:8001/api/docs?chatId=chat-123"
```

### Send Chat Message
```bash
curl -X POST "http://localhost:8001/api/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "chatId": "chat-123",
    "message": "What is the main topic of the document?",
    "userId": "user-456"
  }'
```

### Get Chat History
```bash
curl "http://localhost:8001/api/chats/chat-123/messages"
```

### Delete Chat Session
```bash
curl -X DELETE "http://localhost:8001/api/chats/chat-123"
```

## Logging

The application provides comprehensive logging:
- Console output for development
- File logging to `domain-chatbot-backend.log`
- Structured log format with timestamps and function names
- Different log levels for various components

## Model Configuration

The system uses Hugging Face models:
- **Embeddings**: For document vectorization and semantic search
- **Chat Model**: For generating responses to user queries

Recommended lightweight models for testing:
- Embeddings: `sentence-transformers/all-MiniLM-L6-v2`
- Chat: `google/flan-t5-base`

## Development

### Adding New Endpoints
1. Create route handlers in the `api/` directory
2. Add business logic to `services/`
3. Define Pydantic models in `models.py`
4. Include routers in `main.py`

### Database Integration
The current implementation uses an in-memory database. For production, replace `services/database.py` with a proper database implementation (PostgreSQL, MongoDB, etc.).

### Error Handling
All endpoints include comprehensive error handling with appropriate HTTP status codes and detailed error messages.

## Production Deployment

For production deployment:
1. Set `DEBUG=False` in environment variables
2. Configure proper CORS origins
3. Use a production WSGI server (Gunicorn, uWSGI)
4. Implement proper database persistence
5. Add authentication and authorization
6. Set up monitoring and alerting

## License

This project is licensed under the MIT License.
