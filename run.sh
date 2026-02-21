#!/bin/bash

# Medical Report Analyzer - Startup Script

set -e

echo "🏥 Starting Medical Report Analyzer..."

# Function to check if a port is in use
check_port() {
    netstat -tuln 2>/dev/null | grep -q ":$1 " || \
    lsof -i :$1 2>/dev/null | grep -q LISTEN || \
    return 1
}

# Check if Ollama is running
if ! check_port 11434; then
    echo "⚠️  Ollama is not running on port 11434"
    echo "   Please start Ollama: ollama serve"
    echo ""
fi

# Install dependencies if needed
if [ ! -d "venv" ] && [ ! -d ".venv" ]; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
fi

# Ensure directories exist
echo "📁 Creating directories..."
mkdir -p uploads vector_db

# Start the backend
if ! check_port 8000; then
    echo "🚀 Starting backend server on port 8000..."
    uvicorn backend.app.main:app --reload &
    BACKEND_PID=$!
    sleep 3
else
    echo "✅ Backend already running on port 8000"
fi

# Start the frontend
if ! check_port 8501; then
    echo "🎨 Starting Streamlit frontend on port 8501..."
    streamlit run frontend/app.py &
    FRONTEND_PID=$!
else
    echo "✅ Frontend already running on port 8501"
fi

echo ""
echo "✅ Medical Report Analyzer is running!"
echo "   Backend API: http://localhost:8000"
echo "   Frontend:    http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for interrupt
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null" EXIT
wait
