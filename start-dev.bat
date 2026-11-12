@echo off
setlocal
cd /d "%~dp0frontend"
if not exist "node_modules\vite\bin\vite.js" (
  echo Installing frontend dependencies...
  npm install || exit /b 1
)
echo Opening MineSafe at http://localhost:5173
npm run dev
