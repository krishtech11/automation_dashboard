import os
import pytesseract
import cv2
import numpy as np
from typing import Dict, Any
import tempfile
from PIL import Image
import fitz  # PyMuPDF for PDF handling
from app.config import settings

# Uncomment and update this if needed to specify Tesseract path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def preprocess_image(image_data: bytes) -> np.ndarray:
    """
    Preprocess the image for better OCR results.
    """
    try:
        nparr = np.frombuffer(image_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        kernel = np.ones((1, 1), np.uint8)
        gray = cv2.dilate(gray, kernel, iterations=1)
        gray = cv2.erode(gray, kernel, iterations=1)
        return gray
    except Exception as e:
        raise Exception(f"Error preprocessing image: {str(e)}")

def extract_text_from_image(image_data: bytes) -> str:
    """
    Extract text from an image using Tesseract OCR.
    """
    try:
        processed_img = preprocess_image(image_data)
        text = pytesseract.image_to_string(processed_img)
        return text.strip()
    except Exception as e:
        raise Exception(f"Error extracting text from image: {str(e)}")

def extract_text_from_pdf(pdf_data: bytes) -> str:
    """
    Extract text from PDF using PyMuPDF.
    """
    tmp_pdf_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
            tmp_pdf.write(pdf_data)
            tmp_pdf_path = tmp_pdf.name
        
        text = ""
        with fitz.open(tmp_pdf_path) as doc:
            for page in doc:
                text += page.get_text()
        
        return text.strip()
    except Exception as e:
        raise Exception(f"Error extracting text from PDF: {str(e)}")
    finally:
        if tmp_pdf_path and os.path.exists(tmp_pdf_path):
            os.remove(tmp_pdf_path)

def process_document(file_data: bytes, file_extension: str) -> Dict[str, Any]:
    """
    Process a document and extract text depending on file type.
    """
    try:
        if file_extension.lower() == 'pdf':
            text = extract_text_from_pdf(file_data)
        else:
            text = extract_text_from_image(file_data)
        
        return {
            "status": "success",
            "extracted_text": text,
            "characters_extracted": len(text)
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

def extract_text_from_document(file_data: bytes, content_type: str) -> Dict[str, Any]:
    """
    Main entry function to extract text from supported documents/images.
    """
    supported_types = {
        'application/pdf': 'pdf',
        'image/jpeg': 'jpg',
        'image/png': 'png',
        'image/jpg': 'jpg'
    }
    if content_type.lower() not in supported_types:
        return {
            "status": "error",
            "message": f"Unsupported file type: {content_type}"
        }
    file_extension = supported_types[content_type.lower()]
    return process_document(file_data, file_extension)


import tempfile
import subprocess
import os

def open_text_in_notepad(text: str):
    # Create a temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="w", encoding="utf-8") as tmp_file:
        tmp_file.write(text)
        tmp_path = tmp_file.name
    
    # Open Notepad with the temp file
    subprocess.Popen(['notepad.exe', tmp_path])

    return tmp_path


