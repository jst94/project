@echo off
echo ========================================
echo    PoE Craft Helper - Build Script
echo ========================================
echo.

echo Installing dependencies...
pip install pyinstaller opencv-python pytesseract Pillow numpy requests --break-system-packages

echo.
echo Building executable...
python -m PyInstaller --clean --onefile --windowed --name=PoE_Craft_Helper poe_craft_helper.py

echo.
echo Creating portable package...
if not exist "PoE_Craft_Helper_Portable" mkdir PoE_Craft_Helper_Portable
copy "dist\PoE_Craft_Helper.exe" "PoE_Craft_Helper_Portable\"
copy "README.md" "PoE_Craft_Helper_Portable\" 2>nul

echo.
echo ========================================
echo    BUILD COMPLETE!
echo ========================================
echo.
echo Your executable is ready:
echo - dist\PoE_Craft_Helper.exe
echo - PoE_Craft_Helper_Portable\PoE_Craft_Helper.exe
echo.
echo The portable version can be copied to any Windows PC
echo and run without installing Python or any dependencies.
echo.
pause 
