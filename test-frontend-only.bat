@echo off
echo Testing Frontend Analytics System...
echo.

cd frontend

echo Checking if CSV file exists...
if exist "..\restaurant_dataset_combined.csv" (
    echo ✓ CSV file found
) else (
    echo ✗ CSV file not found
    echo Please ensure restaurant_dataset_combined.csv is in the root directory
    pause
    exit /b 1
)

echo.
echo Starting Flask development server...
echo Open http://localhost:5000 in your browser
echo.
echo Available test URLs:
echo - http://localhost:5000/api/health (Health check)
echo - http://localhost:5000/analysis/peak-dining (Peak Dining Analysis)
echo - http://localhost:5000/analysis/customer-demographics (Customer Demographics)
echo - http://localhost:5000/analysis/menu-analysis (Menu Analysis)
echo - http://localhost:5000/analysis/revenue-analysis (Revenue Analysis)
echo.

python app.py

pause