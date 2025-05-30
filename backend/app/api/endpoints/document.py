from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services import document_automation
from app.config import settings

import threading

router = APIRouter()

@router.post("/document/extract-text")
async def extract_text_from_document(
    file: UploadFile = File(...)
):
    try:
        file_contents = await file.read()
        
        if len(file_contents) > settings.MAX_UPLOAD_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File size exceeds maximum allowed size of {settings.MAX_UPLOAD_SIZE} bytes"
            )
        
        content_type = file.content_type
        if content_type not in settings.ALLOWED_FILE_TYPES:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type. Allowed types: {', '.join(settings.ALLOWED_FILE_TYPES)}"
            )
        
        # Call the main document automation function
        result = document_automation.extract_text_from_document(
            file_data=file_contents,
            content_type=content_type
        )
        
        if result.get("status") == "error":
            raise HTTPException(status_code=400, detail=result.get("message", "Text extraction failed"))

        extracted_text = result.get("extracted_text", "")

        # Open extracted text in Notepad in a background thread
        def open_notepad():
            try:
                document_automation.open_text_in_notepad(extracted_text)
            except Exception as e:
                print(f"Failed to open Notepad: {e}")

        threading.Thread(target=open_notepad).start()
        
        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
