@echo off
cls
color 0A
echo.
echo  ========================================================
echo   🚀 RestaurantIQ Analytics System - Startup Script
echo  ========================================================
echo.
echo  📊 Loading restaurant data...
echo  🏪 Initializing 4 outlets...
echo  📈 Starting analytics engine...
echo.
echo  --------------------------------------------------------
echo   System Information:
echo  --------------------------------------------------------
echo   • Data Records: 8,458 orders
echo   • Active Outlets: 4 restaurants
echo   • Analytics Modules: 7 modules
echo   • Heatmaps: 5 visualizations
echo  --------------------------------------------------------
echo.
echo  🌐 Server will start at: http://localhost:5002
echo.
echo  📍 Quick Access URLs:
echo     Dashboard:  http://localhost:5002/
echo     Analytics:  http://localhost:5002/analysis/peak-dining
echo     Reports:    http://localhost:5002/reports
echo     Test Page:  http://localhost:5002/test
echo.
echo  ⚠️  Press CTRL+C to stop the server
echo  ========================================================
echo.

cd frontend
python app_fixed.py

echo.
echo  ========================================================
echo   Server stopped. Press any key to exit...
echo  ========================================================
pause > nul
