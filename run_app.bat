@echo off
echo Starting Chatbot Application...

:: Start Backend
echo Starting Backend Server...
start "Chatbot Backend" cmd /k "cd backend && uvicorn app.main:app --reload"

:: Wait a moment for backend to initialize (optional but helpful)
timeout /t 2 /nobreak >nul

:: Start Frontend
echo Starting Frontend...
start "Chatbot Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo Both services are starting in separate windows.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:5173
echo.
pause
