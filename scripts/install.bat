@echo off
echo Installing Roblox Fishing Macro Dependencies...
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH!
    echo Please install Python 3.8 or higher from python.org
    pause
    exit /b 1
)

echo Python found. Installing packages...
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ERROR: Failed to install dependencies!
    pause
    exit /b 1
)

echo.
echo ========================================
echo Installation completed successfully!
echo ========================================
echo.
echo Next steps:
echo 1. Place 'point.png' and 'caught.png' in this folder
echo 2. Start Roblox and load the game
echo 3. Run: python background_fishing_macro.py
echo.
pause
