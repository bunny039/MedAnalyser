"""
Document Intake Agent

Accepts uploaded medical documents, validates format, assigns document ID,
and sends to ingestion tool.
"""

import uuid
from typing import List
from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel

router = APIRouter()

# Allowed file extensions for medical documents
ALLOWED_EXTENSIONS = {'.pdf', '.doc', '.docx', '.txt', '.jpg', '.jpeg', '.png'}
ALLOWED_MIME_TYPES = {
    'application/pdf',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'text/plain',
    'image/jpeg',
    'image/png'
}


class DocumentResponse(BaseModel):
    """Response model for document upload"""
    document_id: str
    status: str


def validate_file_format(file: UploadFile) -> bool:
    """
    Validate the file format based on extension and MIME type.
    
    Args:
        file: FastAPI UploadFile object
        
    Returns:
        True if file format is valid
        
    Raises:
        HTTPException: If file format is invalid
    """
    # Check filename
    if not file.filename:
        raise HTTPException(status_code=400, detail="Invalid filename")
    
    # Get file extension
    file_ext = file.filename.lower().split('.')[-1] if '.' in file.filename else ''
    
    # Check extension
    if f'.{file_ext}' not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"File format not allowed. Allowed formats: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # Check MIME type if available
    if file.content_type and file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid MIME type: {file.content_type}"
        )
    
    return True


def generate_document_id() -> str:
    """
    Generate a unique document ID.
    
    Returns:
        Unique document ID string
    """
    return str(uuid.uuid4())


def send_to_ingestion(document_id: str, file: UploadFile) -> bool:
    """
    Send document to ingestion tool.
    
    This is a placeholder for the actual ingestion process.
    
    Args:
        document_id: Unique identifier for the document
        file: The uploaded file
        
    Returns:
        True if ingestion was successful
    """
    # TODO: Implement actual ingestion logic
    # This could involve:
    # - Saving the file to storage
    # - Sending to a document processing service
    # - Adding to a processing queue
    
    print(f"Document {document_id} ({file.filename}) sent to ingestion")
    return True


@router.post("/upload", response_model=DocumentResponse)
async def upload_document(file: UploadFile = File(...)):
    """
    Upload a medical document.
    
    Validates the file format, assigns a unique document ID,
    and sends the document to the ingestion tool.
    
    Args:
        file: The uploaded medical document
        
    Returns:
        DocumentResponse with document_id and status
        
    Raises:
        HTTPException: If file validation fails
    """
    # Validate file format
    validate_file_format(file)
    
    # Generate unique document ID
    document_id = generate_document_id()
    
    # Send to ingestion tool
    try:
        send_to_ingestion(document_id, file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {str(e)}")
    
    # Return response
    return DocumentResponse(
        document_id=document_id,
        status="ingested"
    )


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
