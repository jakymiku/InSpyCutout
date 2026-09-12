@echo off
setlocal EnableExtensions
cd /d "%~dp0"

set "PS_EXE=powershell.exe"
where pwsh.exe >nul 2>nul
if not errorlevel 1 set "PS_EXE=pwsh.exe"

set "SETUP_SCRIPT=%~dp0setup.ps1"
set "SETUP_LOG=%~dp0setup.log"

"%PS_EXE%" -NoLogo -NoProfile -ExecutionPolicy Bypass -Command "try { & $env:SETUP_SCRIPT *>&1 | Tee-Object -FilePath $env:SETUP_LOG; exit 0 } catch { $_ | Out-String | Tee-Object -FilePath $env:SETUP_LOG -Append | Write-Host; exit 1 }"
if errorlevel 1 (
  echo.
  echo Setup failed. See the messages above and setup.log.
  pause
  exit /b 1
)

exit /b 0
