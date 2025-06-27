@echo off
echo Starting test build script...
echo.
echo Current directory: %cd%
echo Script location: %~dp0
echo.
echo Changing to script directory...
cd /d "%~dp0"
echo Now in: %cd%
echo.
echo Checking Python...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python not found
    pause
    exit /b 1
)
echo Python is available
echo.
echo Press any key to continue...
pause
echo Script completed successfully
pause
exit /b 0