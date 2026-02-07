@echo off
echo ========================================
echo 🚀 RESTAURANT ANALYTICS SYSTEM - FIXED
echo ========================================
echo.

echo ✅ PROBLEM IDENTIFIED AND SOLVED:
echo    - Port 5000 was occupied by another service
echo    - Using port 5002 for the analytics system
echo    - All analytics modules now working with REAL DATA
echo.

echo 📊 SYSTEM FEATURES:
echo    - 6,958 restaurant order records loaded
echo    - 7 analytics modules with interactive charts
echo    - Real-time data visualization
echo    - Export capabilities
echo.

cd frontend

echo 🔧 Starting the analytics system...
echo.
echo 🌐 SYSTEM URLS (open in your browser):
echo.
echo 📋 TEST PAGE:     http://localhost:5002/test
echo 🏠 MAIN DASHBOARD: http://localhost:5002/
echo.
echo 📊 ANALYTICS MODULES:
echo    • Peak Dining:     http://localhost:5002/analysis/peak-dining
echo    • Customer Demo:   http://localhost:5002/analysis/customer-demographics  
echo    • Menu Analysis:   http://localhost:5002/analysis/menu-analysis
echo    • Revenue:         http://localhost:5002/analysis/revenue-analysis
echo    • Branch Perf:     http://localhost:5002/analysis/branch-performance
echo    • Anomaly Det:     http://localhost:5002/analysis/anomaly-detection
echo    • Seasonal:        http://localhost:5002/analysis/seasonal-behavior
echo.
echo 🔧 DEBUG URLS:
echo    • Health Check:    http://localhost:5002/api/health
echo    • Data Status:     http://localhost:5002/debug/data-status
echo.

python app_fixed.py

pause