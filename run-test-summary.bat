@echo off
cls
echo ========================================
echo UBER EATS RESTAURANT ANALYTICS SYSTEM
echo TESTING SUMMARY REPORT
echo ========================================
echo.

type test-results-summary.txt

echo.
echo ========================================
echo DETAILED TEST EXECUTION
echo ========================================
echo.
echo Would you like to run detailed tests?
echo 1. Run Frontend Tests Only
echo 2. Run Backend Tests Only  
echo 3. Run All Tests
echo 4. Exit
echo.
set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" (
    echo.
    echo Running Frontend Tests...
    call run-frontend-tests.bat
) else if "%choice%"=="2" (
    echo.
    echo Running Backend Tests...
    call run-backend-tests.bat
) else if "%choice%"=="3" (
    echo.
    echo Running All Tests...
    call run-all-tests.bat
) else (
    echo Exiting...
)

pause