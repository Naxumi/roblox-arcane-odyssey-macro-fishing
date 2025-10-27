@echo off
echo ========================================
echo Roblox Fishing Macro - Installation
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH!
    echo.
    echo Please install Python 3.8 or higher from python.org
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo [OK] Python found
python --version
echo.

REM Go to project root directory
cd /d "%~dp0.."
echo Working directory: %CD%
echo.

REM Check if requirements.txt exists
if not exist "requirements.txt" (
    echo ERROR: requirements.txt not found!
    echo Make sure you're running this from the scripts folder in the project directory.
    pause
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist ".venv" (
    echo Creating virtual environment (.venv)...
    python -m venv .venv
    if errorlevel 1 (
        echo.
        echo ERROR: Failed to create virtual environment!
        echo Make sure you have venv module installed.
        echo.
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created
    echo.
) else (
    echo [OK] Virtual environment already exists
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo.
    echo ERROR: Failed to activate virtual environment!
    echo.
    pause
    exit /b 1
)
echo [OK] Virtual environment activated
echo.

echo Installing Python packages from requirements.txt...
echo.
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ERROR: Failed to install dependencies!
    echo.
    echo Try running these commands manually:
    echo .venv\Scripts\activate.bat
    echo pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo Installation completed successfully!
echo ========================================
echo.
echo IMPORTANT: Virtual environment is now activated (.venv)
echo.
echo Next steps:
echo.
echo 1. Run the setup wizard:
echo    python setup_wizard.py
echo.
echo 2. Or manually create config.py:
echo    copy config.example.py config.py
echo    (Then edit config.py with your settings)
echo.
echo 3. Prepare detection images (IMPORTANT!):
echo    - The provided images may NOT work for your resolution
echo    - You may need to retake screenshots at YOUR resolution
echo    - See README.md for detailed instructions
echo.
echo 4. Run the macro (always activate venv first):
echo    .venv\Scripts\activate.bat
echo    python background_fishing_macro.py
echo.
echo NOTE: Always activate the virtual environment before running:
echo    .venv\Scripts\activate.bat
echo.
echo For detailed setup instructions, read README.md
echo.
pause
