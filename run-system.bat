@echo off
echo Starting Complete Restaurant Analytics System...

echo Starting Backend...
start "Backend" cmd /k "cd backend && mvn spring-boot:run"

echo Waiting for backend to start...
timeout /t 30 /nobreak

echo Starting Frontend...
start "Frontend" cmd /k "cd frontend && python app.py"

echo.
echo System is starting up...
echo Backend: http://localhost:8080
echo Frontend: http://localhost:5000
echo.
echo Wait for both services to fully start, then open http://localhost:5000
pause