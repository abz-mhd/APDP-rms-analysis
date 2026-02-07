@echo off
echo ========================================
echo FRONTEND TESTING RESULTS
echo ========================================
echo.

cd frontend

echo [1/6] Running Unit Tests...
python -m pytest tests/test_unit.py -v --tb=short
echo.

echo [2/6] Running Integration Tests...
python -m pytest tests/test_integration.py -v --tb=short
echo.

echo [3/6] Running System Tests...
python -m pytest tests/test_system.py -v --tb=short
echo.

echo [4/6] Running Performance Tests...
python -m pytest tests/test_performance.py -v --tb=short
echo.

echo [5/6] Running Regression Tests...
python -m pytest tests/test_regression.py -v --tb=short
echo.

echo [6/6] Running Automated Tests...
python -m pytest tests/test_automated.py -v --tb=short
echo.

echo ========================================
echo FRONTEND TESTING COMPLETED
echo ========================================

cd ..
pause