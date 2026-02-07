@echo off
echo ========================================
echo   RestaurantIQ Analytics System
echo ========================================
echo.
echo Starting server...
echo.
echo Dashboard will be available at:
echo   http://localhost:5002
echo.
echo Press CTRL+C to stop the server
echo ========================================
echo.

cd frontend
python app_fixed.py

pause
