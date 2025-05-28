import os
import pytesseract
import cv2
import numpy as np
from typing import Dict, Any, Tuple
import tempfile
from PIL import Image
import io
import fitz  # PyMuPDF for PDF handling

# Configure Tesseract path (update this in your config)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def preprocess_image(image_data: bytes) -> np.ndarray:
    """
    Preprocess the image for better OCR results.
    
    Args:
        image_data: Binary image data
        
    Returns:
        Preprocessed image as a numpy array
    """
    try:
        # Convert bytes to numpy array
        nparr = np.frombuffer(image_data, np.uint8)
        
        # Read image with OpenCV
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Apply thresholding to preprocess the image
        gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        
        # Apply dilation and erosion to remove noise
        kernel = np.ones((1, 1), np.uint8)
        gray = cv2.dilate(gray, kernel, iterations=1)
        gray = cv2.erode(gray, kernel, iterations=1)
        
        return gray
    except Exception as e:
        raise Exception(f"Error preprocessing image: {str(e)}")

def extract_text_from_image(image_data: bytes) -> str:
    """
    Extract text from an image using Tesseract OCR.
    
    Args:
        image_data: Binary image data
        
    Returns:
        Extracted text
    """
    try:
        # Preprocess the image
        processed_img = preprocess_image(image_data)
        
        # Use Tesseract to extract text
        text = pytesseract.image_to_string(processed_img)
        
        return text.strip()
    except Exception as e:
        raise Exception(f"Error extracting text from image: {str(e)}")

def extract_text_from_pdf(pdf_data: bytes) -> str:
    """
    Extract text from a PDF file.
    
    Args:
        pdf_data: Binary PDF data
        
    Returns:
        Extracted text
    """
    try:
        # Create a temporary file to store the PDF
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_pdf:
            temp_pdf.write(pdf_data)
            temp_pdf_path = temp_pdf.name
        
        text = ""
        
        try:
            # Open the PDF
            doc = fitz.open(temp_pdf_path)
            
            # Extract text from each page
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                text += page.get_text()
                
                # If no text was extracted, try OCR on the page image
                if not text.strip():
                    pix = page.get_pixmap()
                    img_data = pix.tobytes("png")
                    text += extract_text_from_image(img_data) + "\n\n"
            
            return text.strip()
        finally:
            # Clean up the temporary file
            if os.path.exists(temp_pdf_path):
                os.unlink(temp_pdf_path)
    except Exception as e:
        raise Exception(f"Error extracting text from PDF: {str(e)}")

def process_document(file_data: bytes, file_extension: str) -> Dict[str, Any]:
    """
    Process a document and extract text.
    
    Args:
        file_data: Binary file data
        file_extension: File extension (e.g., 'pdf', 'jpg', 'png')
        
    Returns:
        Dict containing the extracted text and processing status
    """
    try:
        # Determine the file type and process accordingly
        if file_extension.lower() == 'pdf':
            text = extract_text_from_pdf(file_data)
        else:
            # For image files
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
    Main function to extract text from a document or image.
    
    Args:
        file_data: Binary file data
        content_type: MIME type of the file (e.g., 'application/pdf', 'image/jpeg')
        
    Returns:
        Dict containing the extracted text and processing status
    """
    try:
        # Validate file type
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
        
        # Process the document
        file_extension = supported_types[content_type.lower()]
        return process_document(file_data, file_extension)
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error processing document: {str(e)}"
        }
