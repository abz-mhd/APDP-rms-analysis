@echo off
echo ========================================
echo Testing Analytics System Fix
echo ========================================
echo.

echo 1. Checking file structure...
if exist "restaurant_dataset_combined.csv" (
    echo ✓ CSV dataset found
) else (
    echo ✗ CSV dataset missing
    echo Please ensure restaurant_dataset_combined.csv is in the root directory
    pause
    exit /b 1
)

if exist "frontend\routes\charts.py" (
    echo ✓ Charts routes created
) else (
    echo ✗ Charts routes missing
)

if exist "frontend\data_processor.py" (
    echo ✓ Data processor found
) else (
    echo ✗ Data processor missing
)

echo.
echo 2. Starting frontend server...
cd frontend

echo Testing data loading...
python -c "from data_processor import data_processor; print(f'Data loaded: {len(data_processor.df)} records')"

if %ERRORLEVEL% NEQ 0 (
    echo ✗ Data loading failed
    pause
    exit /b 1
) else (
    echo ✓ Data loading successful
)

echo.
echo 3. Starting Flask server...
echo Open these URLs to test:
echo - http://localhost:5000/debug/data-status (Data status)
echo - http://localhost:5000/api/health (Health check)
echo - http://localhost:5000/analysis/peak-dining (Peak Dining)
echo - http://localhost:5000/analysis/customer-demographics (Customer Demographics)
echo - http://localhost:5000/analysis/menu-analysis (Menu Analysis)
echo - http://localhost:5000/analysis/revenue-analysis (Revenue Analysis)
echo.

python app.py

pause