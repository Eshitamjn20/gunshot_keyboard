$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
python -m venv .venv
if ($LASTEXITCODE -ne 0) { throw 'Could not create Python environment' }
& .\.venv\Scripts\python.exe -m pip install -r requirements-build.txt
if ($LASTEXITCODE -ne 0) { throw 'Could not install build tools' }
& .\.venv\Scripts\python.exe -m PyInstaller --noconfirm --clean --onefile --windowed --name KeyBang app.py
if ($LASTEXITCODE -ne 0) { throw 'Build failed' }
Write-Host 'Ready to share: dist\KeyBang.exe'
