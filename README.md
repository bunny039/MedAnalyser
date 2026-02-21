# Medical Report Analyzer

AI-powered medical report analysis system using RAG (Retrieval Augmented Generation) with Ollama LLM.

## Features

- 📤 Upload medical documents (PDF, DOCX, TXT, images)
- 💬 Chat with your medical reports
- 🔍 Query specific information from reports
- 📋 Generate medical report summaries
- 🏥 AI-powered medical insights

## Tech Stack

- **Backend**: FastAPI + Python
- **Frontend**: Streamlit
- **LLM**: Ollama (llama3)
- **Vector DB**: ChromaDB
- **Embeddings**: Sentence Transformers

## Project Structure

```
medical-report-analyzer/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI entry point
│   │   ├── config.py            # Configuration
│   │   └── dependencies.py     # Shared dependencies
│   ├── api/
│   │   ├── routes_upload.py     # Upload documents
│   │   ├── routes_query.py      # Ask questions
│   │   ├── routes_summary.py   # Generate summaries
│   │   └── routes_chat.py      # Conversational interface
│   ├── core/
│   │   ├── rag_pipeline.py     # RAG pipeline
│   │   ├── ollama_client.py     # Ollama integration
│   │   ├── embeddings.py       # Create embeddings
│   │   ├── retriever.py         # Retrieve chunks
│   │   ├── chunking.py          # Split documents
│   │   └── prompt_templates.py # Prompt templates
│   ├── services/
│   │   ├── document_loader.py   # Load PDFs, DOCX, TXT
│   │   ├── vector_store.py      # ChromaDB/FAISS
│   │   ├── medical_analyzer.py # Medical insights
│   │   └── risk_detector.py    # Risk detection
│   ├── models/
│   │   ├── request_models.py   # Request schemas
│   │   └── response_models.py  # Response schemas
│   └── utils/
│       ├── file_handler.py
│       ├── logger.py
│       └── helpers.py
├── frontend/
│   └── app.py                   # Streamlit app
├── uploads/                      # User uploaded files
├── vector_db/                    # Vector database
├── models/
│   └── ollama_models.txt        # Ollama models
├── tests/
│   ├── test_upload.py
│   ├── test_query.py
│   └── test_rag.py
├── docker/
│   ├── Dockerfile.backend
│   └── docker-compose.yml
├── requirements.txt
├── .env
└── run.sh
```

## Quick Start

### Prerequisites

- Python 3.11+
- Ollama installed and running
- 8GB+ RAM recommended

### Local Setup

1. **Install dependencies**:
   
```
bash
   pip install -r requirements.txt
   
```

2. **Start Ollama**:
   
```
bash
   ollama serve
   ollama pull llama3
   
```

3. **Run the backend**:
   
```
bash
   uvicorn backend.app.main:app --reload
   
```

4. **Run the frontend**:
   
```
bash
   streamlit run frontend/app.py
   
```

### Using Docker

```
bash
cd docker
docker-compose up --build
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/upload` | POST | Upload medical document |
| `/api/query` | POST | Query documents |
| `/api/chat` | POST | Chat with documents |
| `/api/summary/generate` | POST | Generate summary |
| `/health` | GET | Health check |

## Environment Variables

Create a `.env` file:

```
env
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3
CHROMA_DB_PATH=./vector_db
UPLOAD_DIR=./uploads
CHUNK_SIZE=500
CHUNK_OVERLAP=100
```

## Testing

```
bash
pytest tests/
```

## License

MIT License
