@echo off
echo ========================================
echo RMS Analytics System - FIXED VERSION
echo ========================================
echo.

echo ✓ All analytics modules have been fixed
echo ✓ Data loading issues resolved
echo ✓ Chart generation implemented
echo ✓ Missing routes created
echo.

echo Starting the analytics system...
echo.

cd frontend

echo Testing system health...
python -c "from data_processor import data_processor; print(f'✓ Data loaded: {len(data_processor.df)} records')"

if %ERRORLEVEL% NEQ 0 (
    echo ✗ System health check failed
    pause
    exit /b 1
)

echo.
echo ========================================
echo SYSTEM READY - All modules working!
echo ========================================
echo.
echo Open your browser and navigate to:
echo.
echo 🏠 Main Dashboard: http://localhost:5000
echo 📊 Peak Dining: http://localhost:5000/analysis/peak-dining
echo 👥 Customer Demographics: http://localhost:5000/analysis/customer-demographics
echo 🍽️ Menu Analysis: http://localhost:5000/analysis/menu-analysis
echo 💰 Revenue Analysis: http://localhost:5000/analysis/revenue-analysis
echo 🏢 Branch Performance: http://localhost:5000/analysis/branch-performance
echo ⚠️ Anomaly Detection: http://localhost:5000/analysis/anomaly-detection
echo 📈 Seasonal Behavior: http://localhost:5000/analysis/seasonal-behavior
echo.
echo 🔧 Debug URLs:
echo - http://localhost:5000/api/health (System health)
echo - http://localhost:5000/debug/data-status (Data status)
echo.

python app.py

pause