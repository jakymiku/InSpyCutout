$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

function Write-Step($text) {
    Write-Host "`n==> $text" -ForegroundColor Cyan
}

function Find-Python311 {
    try {
        $p = (& py -3.11 -c "import sys; print(sys.executable)" 2>$null)
        if ($LASTEXITCODE -eq 0 -and $p) { return $p.Trim() }
    } catch {}

    $candidates = @(
        "$env:LOCALAPPDATA\Programs\Python\Python311\python.exe",
        "$env:ProgramFiles\Python311\python.exe"
    )
    foreach ($candidate in $candidates) {
        if (Test-Path $candidate) { return $candidate }
    }

    try {
        $p = (& python -c "import sys; print(sys.executable if sys.version_info[:2] == (3,11) else '')" 2>$null)
        if ($LASTEXITCODE -eq 0 -and $p) { return $p.Trim() }
    } catch {}
    return $null
}

Write-Host "InSpyCutout setup / セットアップ" -ForegroundColor Green
Write-Host "This creates an isolated .venv inside this folder. No ComfyUI installation is required."
Write-Host "このフォルダ内に専用 .venv を作成します。ComfyUI は不要です。"

$python = Find-Python311
if (-not $python) {
    Write-Step "Python 3.11 not found / Python 3.11 が見つかりません"
    $winget = Get-Command winget.exe -ErrorAction SilentlyContinue
    if (-not $winget) {
        Write-Host "Python 3.11 is required. Install it from https://www.python.org/downloads/ and run Setup.bat again." -ForegroundColor Red
        Write-Host "Python 3.11 をインストールしてから Setup.bat を再実行してください。" -ForegroundColor Red
        exit 1
    }
    Write-Host "Installing Python 3.11 with winget... / winget で Python 3.11 をインストールします..."
    & winget install --id Python.Python.3.11 -e --scope user --accept-package-agreements --accept-source-agreements
    if ($LASTEXITCODE -ne 0) { throw "winget failed to install Python 3.11." }
    $python = Find-Python311
    if (-not $python) { throw "Python 3.11 was installed but could not be located. Reopen this folder and run Setup.bat again." }
}

Write-Step "Using Python: $python"
if (-not (Test-Path ".venv\Scripts\python.exe")) {
    & $python -m venv .venv
    if ($LASTEXITCODE -ne 0) { throw "Failed to create .venv" }
}

$venvPython = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
Write-Step "Updating pip"
& $venvPython -m pip install --upgrade pip setuptools wheel
if ($LASTEXITCODE -ne 0) { throw "pip update failed" }

$nvidia = Get-Command nvidia-smi.exe -ErrorAction SilentlyContinue
if ($nvidia) {
    Write-Step "NVIDIA GPU detected - installing CUDA 12.8 PyTorch"
    & $venvPython -m pip install torch torchvision --index-url https://download.pytorch.org/whl/cu128
    if ($LASTEXITCODE -ne 0) { throw "CUDA PyTorch installation failed" }
} else {
    Write-Step "No NVIDIA GPU detected - installing default PyTorch"
    & $venvPython -m pip install torch torchvision
    if ($LASTEXITCODE -ne 0) { throw "PyTorch installation failed" }
}

Write-Step "Installing InSpyCutout dependencies"
& $venvPython -m pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) { throw "Dependency installation failed" }

Write-Step "Preloading InSPyReNet model (first download can take a while)"
& $venvPython tools\preload_model.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "Model preload failed. Setup will continue; InSpyCutout will retry on first use." -ForegroundColor Yellow
}

Write-Step "Creating desktop shortcut"
$shortcutScript = Join-Path $PSScriptRoot "tools\create_shortcut.ps1"
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File $shortcutScript

Write-Host "`nSetup complete / セットアップ完了" -ForegroundColor Green
Write-Host "Launch with Launch_GUI.bat or the desktop shortcut."
Write-Host "Launch_GUI.bat またはデスクトップのショートカットから起動できます。"

$answer = Read-Host "Launch InSpyCutout now? / 今すぐ起動しますか？ [Y/n]"
if ([string]::IsNullOrWhiteSpace($answer) -or $answer -match '^[Yy]') {
    Start-Process (Join-Path $PSScriptRoot ".venv\Scripts\pythonw.exe") -ArgumentList @(
        (Join-Path $PSScriptRoot "InSpyCutout.py"),
        "--config",
        (Join-Path $PSScriptRoot "config.ini")
    ) -WorkingDirectory $PSScriptRoot
}
