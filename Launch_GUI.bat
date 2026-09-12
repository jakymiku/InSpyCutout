@echo off
setlocal EnableExtensions
cd /d "%~dp0"

if not exist ".venv\Scripts\pythonw.exe" (
  echo InSpyCutout environment is not installed yet.
  echo Starting setup...
  call "%~dp0Setup.bat"
  if errorlevel 1 exit /b 1
)

start "" ".venv\Scripts\pythonw.exe" "%~dp0InSpyCutout.py" --config "%~dp0config.ini" %*
