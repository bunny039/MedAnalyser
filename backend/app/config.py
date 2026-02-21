"""
Medical Report Analyzer Configuration
Production-ready config using environment variables and RAG settings
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ============== Ollama LLM Configuration ==============
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")

# ============== Chroma DB Configuration ==============
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "./chroma_db")

# ============== Document Upload Configuration ==============
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "./uploads")

# ============== Text Chunking Configuration ==============
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "500"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "100"))

# ============== Create Required Directories ==============
def ensure_directories():
    """Ensure upload and database directories exist"""
    Path(CHROMA_DB_PATH).mkdir(parents=True, exist_ok=True)
    Path(UPLOAD_DIR).mkdir(parents=True, exist_ok=True)


# Create directories on module import
ensure_directories()
