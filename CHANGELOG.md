# Changelog

## 0.1.0 - 2026-09-13

Initial public preview.

### Background removal and mask editing

- InSPyReNet automatic mask generation
- Live Alpha Gamma, Mask Offset, Mask Blur, Black Threshold, and White Threshold adjustment
- White/black mask painting with adjustable brush size
- Undo / Redo
- Live transparency preview
- External mask export/reload for Paint.NET and other editors
- Existing source transparency is preserved
- EXIF orientation is applied when loading images
- Edited masks with mismatched dimensions are rejected instead of resized automatically

### View controls

- Mouse-wheel zoom
- Move-mode left-drag pan
- Space + left-drag temporary pan while painting
- Middle-mouse pan
- Horizontal/tilt-wheel input is ignored to avoid accidental zoom
- Optional synchronized zoom / pan / fit between the Mask and Transparency Preview panes
- Double-click Fit is disabled on the editable mask while Paint mode is active

### Windows integration

- Japanese / English UI with persisted language selection
- Automatic Paint.NET detection for Microsoft Store and desktop installations
- Windows “Open with…” fallback and custom editor support
- Per-image output folders
- Isolated `.venv` and application-local caches
- Setup logging and first-run model preload
- NVIDIA CUDA acceleration when available, with CPU fallback

### Packaging

- Single-file `InSpyCutout.py` source layout
- GitHub Actions syntax validation and Windows ZIP packaging
- Python bytecode/cache files are excluded from release packages
