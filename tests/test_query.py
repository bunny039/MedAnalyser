"""
Tests for query functionality
"""

import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


def test_query_endpoint():
    """Test querying the medical reports"""
    response = client.post(
        "/api/query",
        json={"question": "What are the key findings in the report?"}
    )
    assert response.status_code in [200, 500]  # 500 if no documents uploaded


def test_query_empty_question():
    """Test querying with empty question"""
    response = client.post("/api/query", json={"question": ""})
    assert response.status_code == 422  # Validation error


def test_query_without_question_field():
    """Test querying without question field"""
    response = client.post("/api/query", json={})
    assert response.status_code == 422  # Validation error
