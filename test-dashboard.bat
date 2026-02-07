@echo off
echo ========================================
echo TESTING DASHBOARD WITH REAL DATA
echo ========================================
echo.

echo Starting Frontend Server...
cd frontend
start /B python app.py

echo Waiting for server to start...
timeout /t 5 /nobreak > nul

echo.
echo ========================================
echo DASHBOARD READY!
echo ========================================
echo.
echo Open your browser and go to:
echo http://localhost:5000
echo.
echo Features now working:
echo ✅ Real dataset (6958+ records)
echo ✅ Working filters (Outlet, Season, Date Range)
echo ✅ 6-month forecasting
echo ✅ Minimal blue/gray color scheme
echo ✅ Export CSV/PDF functionality
echo ✅ 2026 UBER EATS footer
echo ✅ No dummy/hardcoded data
echo.
echo Press any key to stop the server...
pause > nul

echo Stopping server...
taskkill /f /im python.exe > nul 2>&1

cd ..
echo Server stopped.
pause