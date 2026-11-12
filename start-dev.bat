@echo off
setlocal
cd /d "%~dp0"
if not exist "backend\venv\Scripts\python.exe" (
  py -3 -m venv backend\venv || python -m venv backend\venv
  call backend\venv\Scripts\activate.bat
  python -m pip install -r backend\requirements.txt
)
start "Coal Governance API" cmd /k "cd /d ""%~dp0backend"" && call ""%~dp0backend\venv\Scripts\activate.bat"" && uvicorn app.main:app --reload --port 8000"
start "Coal Governance Frontend" cmd /k "cd /d ""%~dp0frontend"" && npm install && npm run dev"
endlocal
