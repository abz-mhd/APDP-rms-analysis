@echo off
echo ========================================
echo COMPLETE TESTING SUITE
echo Uber Eats Restaurant Analytics System
echo ========================================
echo.

echo Starting Frontend Tests...
call run-frontend-tests.bat

echo.
echo Starting Backend Tests...
call run-backend-tests.bat

echo.
echo ========================================
echo ALL TESTS COMPLETED
echo ========================================
echo Check above output for PASS/FAIL results
echo.
pause