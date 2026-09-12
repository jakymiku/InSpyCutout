$ErrorActionPreference = "Stop"
Set-Location -LiteralPath $PSScriptRoot

# Keep a full setup transcript in the app folder so very long pip/build output
# is still available even if the console window scrolls it away.
$setupLog = Join-Path $PSScriptRoot "setup.log"
try { Start-Transcript -Path $setupLog -Force | Out-Null } catch {}

# Keep persistent caches inside the application folder so removing the folder
# removes the virtual environment, model files, and caches together.
$cacheRoot = Join-Path $PSScriptRoot "cache"
$env:PIP_CACHE_DIR = Join-Path $cacheRoot "pip"
$env:TRANSPARENT_BACKGROUND_FILE_PATH = Join-Path $cacheRoot "models"
$env:TORCH_HOME = Join-Path $cacheRoot "torch"
$env:TORCH_EXTENSIONS_DIR = Join-Path $cacheRoot "torch_extensions"
$env:HF_HOME = Join-Path $cacheRoot "huggingface"
$env:XDG_CACHE_HOME = Join-Path $cacheRoot "xdg"

@($cacheRoot, $env:PIP_CACHE_DIR, $env:TRANSPARENT_BACKGROUND_FILE_PATH, $env:TORCH_HOME, $env:TORCH_EXTENSIONS_DIR, $env:HF_HOME, $env:XDG_CACHE_HOME) | ForEach-Object {
    New-Item -ItemType Directory -Force -Path $_ | Out-Null
}

function Write-Step {
    param([Parameter(Mandatory = $true)][string]$Text)
    Write-Host ""
    Write-Host "==> $Text" -ForegroundColor Cyan
}

function Find-Python311 {
    try {
        $p = & py.exe -3.11 -c "import sys; print(sys.executable)" 2>$null
        if ($LASTEXITCODE -eq 0 -and $p) {
            return ($p | Select-Object -First 1).Trim()
        }
    }
    catch {}

    $candidates = @(
        (Join-Path $env:LOCALAPPDATA "Programs\Python\Python311\python.exe"),
        (Join-Path $env:ProgramFiles "Python311\python.exe")
    )

    foreach ($candidate in $candidates) {
        if ($candidate -and (Test-Path -LiteralPath $candidate)) {
            return $candidate
        }
    }

    try {
        $p = & python.exe -c "import sys; print(sys.executable if sys.version_info[:2] == (3, 11) else '')" 2>$null
        if ($LASTEXITCODE -eq 0 -and $p) {
            $value = ($p | Select-Object -First 1).Trim()
            if ($value) { return $value }
        }
    }
    catch {}

    return $null
}

Write-Host "InSpyCutout setup" -ForegroundColor Green
Write-Host "This creates an isolated .venv inside this folder. ComfyUI is not required."

$python = Find-Python311
if (-not $python) {
    Write-Step "Python 3.11 was not found"
    $winget = Get-Command winget.exe -ErrorAction SilentlyContinue
    if (-not $winget) {
        Write-Host "Python 3.11 is required." -ForegroundColor Red
        Write-Host "Install Python 3.11 from https://www.python.org/downloads/ and run Setup.bat again." -ForegroundColor Red
        exit 1
    }

    Write-Host "Installing Python 3.11 with winget..."
    & $winget.Source install --id Python.Python.3.11 -e --scope user --accept-package-agreements --accept-source-agreements
    if ($LASTEXITCODE -ne 0) {
        throw "winget failed to install Python 3.11."
    }

    $python = Find-Python311
    if (-not $python) {
        throw "Python 3.11 was installed but could not be located. Close this window, reopen the folder, and run Setup.bat again."
    }
}

Write-Step "Using Python: $python"
$venvPython = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
if (-not (Test-Path -LiteralPath $venvPython)) {
    Write-Step "Creating isolated Python environment"
    & $python -m venv (Join-Path $PSScriptRoot ".venv")
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to create .venv."
    }
}

Write-Step "Updating pip"
& $venvPython -m pip install --upgrade pip setuptools wheel
if ($LASTEXITCODE -ne 0) {
    throw "pip update failed."
}

$nvidia = Get-Command nvidia-smi.exe -ErrorAction SilentlyContinue
if ($nvidia) {
    Write-Step "NVIDIA GPU detected - installing CUDA 12.8 PyTorch"
    & $venvPython -m pip install torch torchvision --index-url https://download.pytorch.org/whl/cu128
    if ($LASTEXITCODE -ne 0) {
        throw "CUDA PyTorch installation failed."
    }
}
else {
    Write-Step "No NVIDIA GPU detected - installing default PyTorch"
    & $venvPython -m pip install torch torchvision
    if ($LASTEXITCODE -ne 0) {
        throw "PyTorch installation failed."
    }
}

Write-Step "Installing InSpyCutout dependencies"
& $venvPython -m pip install -r (Join-Path $PSScriptRoot "requirements.txt")
if ($LASTEXITCODE -ne 0) {
    throw "Dependency installation failed."
}

Write-Step "Preloading the InSPyReNet model"
& $venvPython (Join-Path $PSScriptRoot "tools\preload_model.py")
if ($LASTEXITCODE -ne 0) {
    Write-Host "Model preload failed. Setup will continue and InSpyCutout will retry on first use." -ForegroundColor Yellow
}

Write-Step "Creating desktop shortcut"
$shortcutScript = Join-Path $PSScriptRoot "tools\create_shortcut.ps1"
& powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File $shortcutScript
if ($LASTEXITCODE -ne 0) {
    Write-Host "Desktop shortcut creation failed. You can still use Launch_GUI.bat." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Setup complete." -ForegroundColor Green
Write-Host "Setup log: $setupLog"
Write-Host "Launch with Launch_GUI.bat or the desktop shortcut."

try { Stop-Transcript | Out-Null } catch {}

$answer = Read-Host "Launch InSpyCutout now? [Y/n]"
if ([string]::IsNullOrWhiteSpace($answer) -or $answer -match '^[Yy]') {
    $pythonw = Join-Path $PSScriptRoot ".venv\Scripts\pythonw.exe"
    $app = Join-Path $PSScriptRoot "InSpyCutout.py"
    $config = Join-Path $PSScriptRoot "config.ini"
    Start-Process -FilePath $pythonw -ArgumentList @($app, "--config", $config) -WorkingDirectory $PSScriptRoot
}
