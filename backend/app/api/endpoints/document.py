from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import Optional
import os
from app.services import document_automation
from app.config import settings

router = APIRouter()

@router.post("/document/extract-text")
async def extract_text_from_document(
    file: UploadFile = File(...)
):
    """
    Extract text from an uploaded document or image using OCR.
    
    - **file**: The document or image file to process (PDF, JPG, PNG)
    """
    try:
        # Check file size
        file_contents = await file.read()
        if len(file_contents) > settings.MAX_UPLOAD_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File size exceeds maximum allowed size of {settings.MAX_UPLOAD_SIZE} bytes"
            )
        
        # Check file type
        content_type = file.content_type
        if content_type not in settings.ALLOWED_FILE_TYPES:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type. Allowed types: {', '.join(settings.ALLOWED_FILE_TYPES)}"
            )
        
        # Process the document
        result = document_automation.extract_text_from_document(
            file_data=file_contents,
            content_type=content_type
        )
        
        if result.get("status") == "error":
            raise HTTPException(status_code=400, detail=result.get("message", "Text extraction failed"))
            
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
