@echo off
echo Starting Automation Dashboard...
echo.

REM Start the backend server in a new command prompt
start "Backend Server" cmd /k "cd backend && .\venv\Scripts\activate && python -m uvicorn app.main:app --reload"

REM Start the frontend server in a new command prompt
start "Frontend Server" cmd /k "cd frontend && npm start"

echo.
echo Backend server will be available at: http://localhost:8000
echo Frontend will be available at: http://localhost:3000
echo.
pause
