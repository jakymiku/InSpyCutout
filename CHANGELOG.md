# Changelog

## 0.1.0 - 2026-09-12

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
- Fixed mask-source label localization when switching Japanese / English
- Added automatic Paint.NET detection for Store and desktop installs
- Replaced Windows-default PNG launching with an explicit Windows “Open with…” fallback
