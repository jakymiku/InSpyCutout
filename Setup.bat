@echo off
setlocal EnableExtensions
cd /d "%~dp0"

set "PS_EXE=powershell.exe"
where pwsh.exe >nul 2>nul
if not errorlevel 1 set "PS_EXE=pwsh.exe"

set "SETUP_SCRIPT=%~dp0setup.ps1"

rem setup.ps1 owns setup.log via Start-Transcript.
rem Do not Tee-Object to the same file here, or both processes will fight over
rem setup.log and a clean setup can fail with a file-in-use error.
"%PS_EXE%" -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%SETUP_SCRIPT%"
if errorlevel 1 (
  echo.
  echo Setup failed. See the messages above and setup.log.
  pause
  exit /b 1
)

exit /b 0
