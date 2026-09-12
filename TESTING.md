# InSpyCutout release test checklist

This file tracks the practical checks used before publishing a release.

## Setup / packaging

- [x] `Setup.bat` reaches the final launch prompt on a clean extracted folder
- [x] Dedicated `.venv` is created inside the app folder
- [x] App-specific caches are redirected into `cache/`
- [x] Existing cache can be copied into a fresh extracted folder and reused
- [x] `setup.log` is written without BAT/PowerShell file-lock contention
- [x] First-run setup does not create duplicate GUI windows
- [x] GitHub Actions syntax-checks the Python source before packaging
- [x] GitHub Actions produces a Windows ZIP artifact
- [x] Release ZIP contains a normal single `InSpyCutout.py`
- [x] Release ZIP excludes `__pycache__`, `.pyc`, and `.pyo`

## Image / mask handling

- [x] Anime / illustration-style AI images
- [x] Photo-style AI images
- [x] Existing transparent PNG input keeps its original transparency ceiling
- [x] EXIF orientation is applied correctly
- [x] External edited mask with wrong dimensions is rejected instead of resized
- [x] Japanese folder/file names work
- [x] Symbol-heavy Windows folder/file names work

## UI / editing

- [x] Japanese / English UI switching
- [x] Mask-source label updates with the selected language
- [x] Mouse-wheel zoom
- [x] Middle-button pan
- [x] Horizontal/tilt-wheel input does not accidentally zoom
- [x] Paint.NET Microsoft Store detection
- [x] External-mask export/reload workflow
- [x] RC3: double-click Fit is disabled on the editable mask while Paint mode is active
- [x] RC3: double-click Fit still works normally after switching back to Move mode
- [x] RC3: optional Mask / Transparency Preview zoom and pan synchronization works

### Known non-blocking performance note

- When Mask / Transparency Preview view synchronization is enabled and the whole image is visible, synchronized panning can feel slightly less smooth than when zoomed in. This is currently considered non-blocking because the full visible image is redrawn in both panes on each view update; zoomed-in operation is smooth in practical use.

## Before making the repository public

- [ ] Run the latest GitHub Actions artifact on a fresh extracted folder
- [ ] Confirm `Setup.bat` completes with the latest artifact
- [ ] Confirm AI mask generation and save work from that artifact
- [ ] Confirm README and third-party notices match the packaged version
- [ ] Optionally add a sanitized GUI screenshot to the README
- [ ] Create the `v0.1.0` tag only after the final artifact passes
