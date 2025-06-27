@echo off
echo Diagnostic Script for Build Issues
echo ==================================
echo.
echo Press any key at each step to continue...
pause

echo.
echo Step 1: Current directory
echo -------------------------
echo Current dir: %cd%
echo Script location: %~dp0
pause

echo.
echo Step 2: Python check
echo --------------------
where python
python --version
echo Errorlevel: %errorlevel%
pause

echo.
echo Step 3: Directory contents
echo -------------------------
dir /b *.py
pause

echo.
echo Step 4: File existence checks
echo ----------------------------
if exist "launcher.py" (
    echo launcher.py EXISTS
) else (
    echo launcher.py NOT FOUND
)
pause

echo.
echo Step 5: Test simple command
echo --------------------------
echo This is a test
pause

echo.
echo Script completed. Window should stay open.
pause