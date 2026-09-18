@echo off
REM Defect Importer EXE Builder

echo.
echo ===================================
echo Defect Data Importer - EXE Builder
echo ===================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

echo [Step 1] Installing required packages...
pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller

if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo [Step 2] Building EXE...
pyinstaller --onefile ^
    --windowed ^
    --name "Defect_Importer" ^
    --icon=icon.ico ^
    --add-data "defect_importer.py:." ^
    defect_importer.py

if errorlevel 1 (
    echo ERROR: Failed to build EXE
    pause
    exit /b 1
)

echo.
echo ===================================
echo BUILD SUCCESSFUL!
echo ===================================
echo.
echo The EXE file is located at:
echo   .\dist\Defect_Importer.exe
echo.
echo You can now run the application by double-clicking the EXE file.
echo.
pause
