@echo off
setlocal EnableExtensions
cd /d "%~dp0"

set "PS_EXE=powershell.exe"
where pwsh.exe >nul 2>nul
if not errorlevel 1 set "PS_EXE=pwsh.exe"

"%PS_EXE%" -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0setup.ps1"
if errorlevel 1 (
  echo.
  echo Setup failed. See the messages above.
  pause
  exit /b 1
)

exit /b 0
