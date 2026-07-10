$ErrorActionPreference = "Stop"

py -3.11 -m venv .venv
& .\.venv\Scripts\python.exe -m pip install --upgrade pip
& .\.venv\Scripts\python.exe -m pip install -e .

Write-Host "LIMEN is installed. Activate with: .\.venv\Scripts\Activate.ps1"
Write-Host "Then run: limen awaken"
