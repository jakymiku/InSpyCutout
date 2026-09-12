# Changelog

## 0.1.0 - 2026-09-13

Initial public preview.

- InSPyReNet automatic mask generation
- Live alpha gamma / mask offset / blur / black and white threshold tuning
- 0-255 black and white threshold controls with direct numeric input
- Zoom, pan, middle-mouse pan, and Space-to-pan
- Lightweight white/black mask painting with adjustable brush size
- Undo / redo
- Fast live transparency preview while painting
- Export/reload edited masks for external tools such as Paint.NET
- Per-image output folders
- Japanese / English UI switch with persisted language setting
- Windows setup script with isolated `.venv`, dependency installation, model preload, and desktop shortcut
- Pin the Windows dependency chain to transparent-background 1.3.4 / albumentations 1.4.16 / albucore 0.0.17 to avoid StringZilla source-build failures
- Write a persistent `setup.log` during setup for easier troubleshooting
- Fixed `setup.log` file-lock failure by making `setup.ps1` the single log owner instead of writing the same log from both BAT and PowerShell
- Avoid duplicate GUI launches when `Launch_GUI.bat` invokes first-run setup
- Fixed mask-source label localization when switching Japanese / English
- Added automatic Paint.NET detection for Store and desktop installs
- Replaced Windows-default PNG launching with an explicit Windows “Open with…” fallback
- Ignore horizontal/tilt-wheel input and suppress wheel zoom during active panning
- Apply EXIF orientation when loading source images and masks
- Preserve pre-existing source transparency by clamping the final alpha to the source alpha
- Reject mismatched external/edited mask dimensions instead of silently resizing them
- Show checkerboard on the original preview when the source image already contains transparency
- Confirmed Japanese and symbol-heavy Windows paths work in real-world testing
- Expanded the documented target from anime/illustration images to include photo-style AI images and photos
- GitHub Actions validates the Python source before packaging
- Repository source layout is normalized to a single `InSpyCutout.py`
- GitHub Actions release ZIP excludes Python bytecode/cache artifacts
