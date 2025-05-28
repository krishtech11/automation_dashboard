# Automation Dashboard

An all-in-one automation dashboard that combines web, desktop, and document automation capabilities.

## Features

- **Web Automation**: Automate website interactions using Selenium
- **Desktop Automation**: Control desktop applications with PyAutoGUI
- **Document Processing**: Extract text from images and PDFs using Tesseract OCR

## Prerequisites

- Python 3.8+
- Node.js 14+ and npm
- Tesseract OCR (for document processing)
- Chrome or Chromium browser (for web automation)

## Quick Start

### Windows

1. Double-click on `start_servers.bat`
   - This will start both the backend and frontend servers
   - Backend will be available at http://localhost:8000
   - Frontend will be available at http://localhost:3000

### Linux/macOS

1. Make the start script executable:
   ```bash
   chmod +x start_servers.sh
   ```
2. Run the start script:
   ```bash
   ./start_servers.sh
   ```

## Manual Setup

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # On Windows
   # OR
   source venv/bin/activate  # On Linux/macOS
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Install system dependencies:
   - **Windows**: Install Tesseract OCR from [here](https://github.com/UB-Mannheim/tesseract/wiki)
   - **macOS**: `brew install tesseract`
   - **Linux (Debian/Ubuntu)**: `sudo apt install tesseract-ocr`
   - **Linux (Fedora)**: `sudo dnf install tesseract`

5. Run the backend server:
   ```bash
   python -m uvicorn app.main:app --reload
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install Node.js dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

## API Documentation

Once the backend is running, you can access the following endpoints:

- Interactive API documentation: http://localhost:8000/docs
- Alternative documentation: http://localhost:8000/redoc
- OpenAPI schema: http://localhost:8000/openapi.json

## Usage Guide

### Web Automation

1. Go to the Web Automation tab
2. Enter the target website URL
3. If the site requires login, provide username and password
4. (Optional) Enter a search query
5. Click "Run Web Automation"

### Desktop Automation

1. Go to the Desktop Automation tab
2. Select the application you want to automate
3. Choose an action (open, close, or type)
4. If typing, enter the text to type
5. Click "Run Desktop Automation"

### Document Automation

1. Go to the Document Automation tab
2. Upload a PDF, JPG, or PNG file
3. Click "Extract Text"
4. View the extracted text in the results section

## Project Structure

```
automation_dashboard/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── endpoints/
│   │   │       ├── web.py
│   │   │       ├── desktop.py
│   │   │       └── document.py
│   │   ├── services/
│   │   │   ├── web_automation.py
│   │   │   ├── desktop_automation.py
│   │   │   └── document_automation.py
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── main.py
│   └── requirements.txt
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── WebAutomation.tsx
│   │   │   ├── DesktopAutomation.tsx
│   │   │   └── DocumentAutomation.tsx
│   │   ├── App.tsx
│   │   ├── index.css
│   │   └── index.tsx
│   ├── package.json
│   └── tsconfig.json
├── start_servers.bat
├── start_servers.sh
└── README.md
```

## Troubleshooting

### Common Issues

1. **Tesseract OCR not found**
   - Ensure Tesseract is installed and added to your system PATH
   - On Windows, the default path is `C:\\Program Files\\Tesseract-OCR\\tesseract.exe`

2. **ChromeDriver issues**
   - The application uses webdriver-manager to handle ChromeDriver
   - Make sure you have Chrome or Chromium installed

3. **Port already in use**
   - Backend runs on port 8000 by default
   - Frontend runs on port 3000 by default
   - Change these in the respective start commands if needed

## License

This project is open source and available under the [MIT License](LICENSE).

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For support, please open an issue in the GitHub repository.
