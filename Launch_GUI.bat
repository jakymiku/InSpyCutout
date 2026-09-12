@echo off
setlocal EnableExtensions
cd /d "%~dp0"

rem Keep model/package caches local to the InSpyCutout folder.
set "PIP_CACHE_DIR=%~dp0cache\pip"
set "TRANSPARENT_BACKGROUND_FILE_PATH=%~dp0cache\models"
set "TORCH_HOME=%~dp0cache\torch"
set "TORCH_EXTENSIONS_DIR=%~dp0cache\torch_extensions"
set "HF_HOME=%~dp0cache\huggingface"
set "XDG_CACHE_HOME=%~dp0cache\xdg"

if not exist ".venv\Scripts\pythonw.exe" (
  echo InSpyCutout environment is not installed yet.
  echo Starting setup...
  call "%~dp0Setup.bat"
  if errorlevel 1 exit /b 1
)

start "" ".venv\Scripts\pythonw.exe" "%~dp0InSpyCutout.py" --config "%~dp0config.ini" %*
