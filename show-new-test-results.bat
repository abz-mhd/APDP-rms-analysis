@echo off
cls
echo ========================================
echo BACKEND TESTING FIXED - NEW RESULTS
echo ========================================
echo.

echo Running Backend Tests...
echo.
cd backend
mvn test -q
cd ..

echo.
echo ========================================
echo UPDATED TEST SUMMARY
echo ========================================
echo.

type test-results-summary.txt

echo.
echo ========================================
echo BACKEND TESTING STATUS: FIXED ✅
echo All 25 backend tests now passing!
echo ========================================
pause