"""
Tests for RAG pipeline functionality
"""

import pytest
from backend.core.rag_pipeline import RAGPipeline
from backend.core.chunking import chunk_text
from backend.core.retriever import Retriever


def test_chunk_text():
    """Test text chunking"""
    text = "This is a test document. " * 100
    chunks = chunk_text(text, chunk_size=500, chunk_overlap=100)
    assert len(chunks) > 0
    assert all(len(chunk) <= 500 for chunk in chunks)


def test_retriever_initialization():
    """Test retriever initialization"""
    retriever = Retriever()
    assert retriever is not None


def test_rag_pipeline_initialization():
    """Test RAG pipeline initialization"""
    pipeline = RAGPipeline()
    assert pipeline is not None


def test_rag_pipeline_query_without_documents():
    """Test RAG pipeline query without uploaded documents"""
    pipeline = RAGPipeline()
    result = pipeline.query("Test question")
    # Should return a response even without documents
    assert result is not None
