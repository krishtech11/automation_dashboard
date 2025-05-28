#!/bin/bash
echo "Starting Automation Dashboard..."
echo ""

# Start the backend server in the background
(cd backend && source venv/bin/activate && uvicorn app.main:app --reload &)

# Start the frontend server in the background
(cd frontend && npm start &)

echo ""
echo "Backend server will be available at: http://localhost:8000"
echo "Frontend will be available at: http://localhost:3000"
echo ""

# Keep the script running
wait
