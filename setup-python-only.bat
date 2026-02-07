@echo off
echo Setting up Restaurant Analytics System (Python-only version)...

echo.
echo Checking Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo.
echo Installing Python dependencies...
cd frontend
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install Python dependencies
    echo Please check your Python and pip installation
    pause
    exit /b 1
)
cd ..

echo.
echo Python-only setup completed!
echo.
echo NOTE: This version will run the frontend only with mock data.
echo For full functionality, you need to install Java 17+ and Maven.
echo.
echo To start the frontend:
echo 1. Run start-frontend-only.bat
echo 2. Open http://localhost:5000 in your browser
echo.
pause