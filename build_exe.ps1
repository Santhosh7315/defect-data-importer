# Defect Importer EXE Builder (PowerShell)

Write-Host ""
Write-Host "===================================" -ForegroundColor Cyan
Write-Host "Defect Data Importer - EXE Builder" -ForegroundColor Cyan
Write-Host "===================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
try {
    python --version | Out-Null
} catch {
    Write-Host "ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python from https://www.python.org/" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "[Step 1] Installing required packages..." -ForegroundColor Yellow
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install pyinstaller

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to install dependencies" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "[Step 2] Building EXE..." -ForegroundColor Yellow

pyinstaller --onefile `
    --windowed `
    --name "Defect_Importer" `
    defect_importer.py

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to build EXE" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "===================================" -ForegroundColor Green
Write-Host "BUILD SUCCESSFUL!" -ForegroundColor Green
Write-Host "===================================" -ForegroundColor Green
Write-Host ""
Write-Host "The EXE file is located at:" -ForegroundColor Cyan
Write-Host "  .\dist\Defect_Importer.exe" -ForegroundColor White
Write-Host ""
Write-Host "You can now run the application by double-clicking the EXE file." -ForegroundColor Green
Write-Host ""

Read-Host "Press Enter to exit"
