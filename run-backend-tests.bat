@echo off
echo ========================================
echo BACKEND TESTING RESULTS
echo ========================================
echo.

cd backend

echo [1/6] Running Unit Tests...
mvn test -Dtest=UnitTests -q
echo.

echo [2/6] Running Integration Tests...
mvn test -Dtest=IntegrationTests -q
echo.

echo [3/6] Running System Tests...
mvn test -Dtest=SystemTests -q
echo.

echo [4/6] Running Performance Tests...
mvn test -Dtest=PerformanceTests -q
echo.

echo [5/6] Running Regression Tests...
mvn test -Dtest=RegressionTests -q
echo.

echo [6/6] Running Automated Tests...
mvn test -Dtest=AutomatedTests -q
echo.

echo ========================================
echo BACKEND TESTING COMPLETED
echo ========================================

cd ..
pause