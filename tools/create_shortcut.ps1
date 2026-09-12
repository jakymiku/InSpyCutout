$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
$desktop = [Environment]::GetFolderPath("Desktop")
$shortcutPath = Join-Path $desktop "InSpyCutout.lnk"
$target = Join-Path $root "Launch_GUI.bat"

$ws = New-Object -ComObject WScript.Shell
$sc = $ws.CreateShortcut($shortcutPath)
$sc.TargetPath = $target
$sc.WorkingDirectory = $root
$sc.Description = "InSpyCutout - AI-assisted background removal and mask editor"
$sc.Save()
Write-Host "Shortcut created: $shortcutPath"
