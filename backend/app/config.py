from pydantic_settings import BaseSettings
from typing import Optional
from typing import List


class Settings(BaseSettings):
    PROJECT_NAME: str = "Automation Dashboard API"
    VERSION: str = "1.0.0"
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    API_V1_STR: str = "/api"
    
    # Security
    SECRET_KEY: str = "your-secret-key-here"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000"]

    
    # File upload settings
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_FILE_TYPES: list[str] = ["application/pdf", "image/jpeg", "image/png"]
    
    # Tesseract OCR path (update this to your Tesseract installation path)
    TESSERACT_CMD: str = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    
    class Config:
        case_sensitive = True

settings = Settings()
