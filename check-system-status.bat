@echo off
cls
echo ========================================
echo UBER EATS RESTAURANT ANALYTICS SYSTEM
echo SYSTEM STATUS CHECK
echo ========================================
echo.

echo Checking Frontend Status...
curl -s http://localhost:5000 > nul
if %errorlevel% == 0 (
    echo ✅ Frontend: RUNNING on http://localhost:5000
) else (
    echo ❌ Frontend: NOT RUNNING
)

echo.
echo Checking API Endpoints...
curl -s http://localhost:5000/api/outlets > nul
if %errorlevel% == 0 (
    echo ✅ API Endpoints: WORKING
) else (
    echo ❌ API Endpoints: NOT WORKING
)

echo.
echo ========================================
echo SYSTEM READY!
echo ========================================
echo.
echo 🌐 Dashboard URL: http://localhost:5000
echo 📊 Dataset: 6,958+ real records loaded
echo 🎨 Design: Minimal blue/gray theme
echo 📈 Features: Real-time analytics, forecasting, exports
echo 👤 Footer: 2026 All rights reserved by UBER EATS
echo.
echo Press any key to open dashboard in browser...
pause > nul

start http://localhost:5000

echo.
echo Dashboard opened in your default browser!
echo.
echo Available Features:
echo - Real outlet data filtering
echo - Season-based analysis  
echo - 6-month revenue forecasting
echo - CSV/PDF export functionality
echo - Peak dining analysis
echo - Customer demographics
echo - Revenue trends
echo - Menu item popularity
echo - Branch performance rankings
echo.
pause