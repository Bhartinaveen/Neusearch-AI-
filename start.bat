@echo off
echo Starting Neusearch AI...

start "Backend" cmd /k "cd backend && py -m uvicorn app.main:app --reload --port 8000"
start "Frontend" cmd /k "cd frontend && npm run dev"

echo Services started!
echo Backend: http://localhost:8000/docs
echo Frontend: http://localhost:5173
echo.
echo Use Ctrl+C in the windows to stop.
pause
