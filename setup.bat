@echo off
echo Setting up Restaurant Analytics System...

echo.
echo Checking prerequisites...

echo Checking Java...
java -version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Java is not installed or not in PATH
    echo Please install Java 17 or higher from: https://adoptium.net/
    echo.
    pause
    exit /b 1
)

echo Checking Maven...
mvn -version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Maven is not installed or not in PATH
    echo Please install Maven from: https://maven.apache.org/download.cgi
    echo.
    pause
    exit /b 1
)

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
echo All prerequisites found!
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
echo Compiling Java backend...
cd backend
mvn compile
if %errorlevel% neq 0 (
    echo ERROR: Failed to compile Java backend
    echo Please check the error messages above
    pause
    exit /b 1
)
cd ..

echo.
echo Setup completed successfully!
echo.
echo To start the system:
echo 1. Run start-backend.bat (wait for it to fully start)
echo 2. Run start-frontend.bat
echo 3. Open http://localhost:5000 in your browser
echo.
echo Or run run-system.bat to start both services automatically
echo.
pause