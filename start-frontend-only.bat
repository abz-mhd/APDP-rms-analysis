@echo off
echo Starting Restaurant Analytics Frontend (Mock Data Mode)...
echo.
echo NOTE: Backend is not running. The frontend will show mock data.
echo For full functionality, install Java 17+ and Maven, then run the full system.
echo.
cd frontend
python app-mock.py
pause