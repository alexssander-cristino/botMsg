@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo Ambiente virtual nao encontrado.
  echo Execute primeiro: py -m venv .venv
  echo Depois: .venv\Scripts\activate e pip install -r requirements.txt
  pause
  exit /b 1
)
".venv\Scripts\python.exe" app.py
pause
