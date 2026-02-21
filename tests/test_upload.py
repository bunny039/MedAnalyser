"""
Tests for document upload functionality
"""

import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_upload_document_pdf():
    """Test uploading a PDF document"""
    files = {"file": ("test_report.pdf", b"PDF content", "application/pdf")}
    response = client.post("/api/upload", files=files)
    assert response.status_code == 200
    data = response.json()
    assert "document_id" in data
    assert data["status"] == "ingested"


def test_upload_document_invalid_format():
    """Test uploading an invalid file format"""
    files = {"file": ("test.exe", b"exe content", "application/octet-stream")}
    response = client.post("/api/upload", files=files)
    assert response.status_code == 400


def test_upload_empty_filename():
    """Test uploading a file with empty filename"""
    files = {"file": ("", b"content", "text/plain")}
    response = client.post("/api/upload", files=files)
    assert response.status_code == 400
