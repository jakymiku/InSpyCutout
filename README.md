# InSpyCutout

**A lightweight, local, AI-assisted background remover and mask editor for anime, illustrations, AI images, and photos.**

[日本語 README](README_ja.md)

InSpyCutout uses **InSPyReNet** through `transparent-background` to generate a soft foreground mask, then lets you quickly fix the small mistakes that fully automatic removal often leaves behind.

The intended workflow is simple:

1. Open an image.
2. InSpyReNet creates a mask automatically.
3. Fine-tune alpha gamma, thresholds, blur, or mask offset while watching the transparency preview.
4. Paint white to keep pixels or black to remove them for quick corrections.
5. Save the cutout. For larger edits, export the mask to Paint.NET or another editor and reload it.

## Highlights

- Fully local processing after model setup
- App-specific model/package caches are kept inside the InSpyCutout folder
- InSpyReNet `base` model by default
- Works well with anime/illustration images and can also handle photo-style images
- Live transparency preview
- White/black quick mask painting
- Adjustable brush size, Undo / Redo
- Mouse-wheel zoom
- Left-drag pan in Move mode
- Hold **Space** + left-drag to temporarily pan while painting
- Middle-mouse drag to pan at any time
- Black / White Threshold controls from 0 to 255
- Japanese / English UI toggle
- Output organized as `output/<source filename>/...`
- Automatic Paint.NET detection (Microsoft Store / desktop) plus Windows “Open with…” fallback
- EXIF orientation is applied automatically for camera/smartphone images
- Existing source transparency is preserved and cannot be accidentally made opaque by the generated mask
- External/edited masks with the wrong dimensions are rejected instead of silently resized

## Recommended environment

| Item | Recommendation / notes |
|---|---|
| OS | 64-bit Windows 10 or Windows 11 |
| Python | Python 3.11. Setup can install it automatically with `winget` when available. |
| GPU | **NVIDIA CUDA-capable GPU recommended.** This provides by far the best mask-generation speed. |
| CPU-only use | Supported. Systems without a supported NVIDIA GPU can run InSpyCutout on the CPU, but AI mask generation can be substantially slower. |
| AMD / Intel GPU | The current Windows setup does not configure AMD or Intel GPU acceleration, so these systems currently use CPU inference. |
| Memory | 16 GB RAM or more is recommended for comfortable use. |
| Disk space | Several GB of free space is required for PyTorch, the Python environment, the InSPyReNet model, and local caches. Extra free space is recommended during setup. |
| Internet | Required for the initial setup and model/package downloads. After setup, normal image processing is local. |

On NVIDIA systems, Setup installs the official PyTorch **CUDA 12.8** build. A reasonably current NVIDIA driver is therefore recommended. There is currently no hard VRAM minimum documented because it has not been broadly tested across GPU models; if GPU execution is unavailable, InSpyCutout falls back to CPU operation rather than requiring CUDA.

## Windows quick start

1. Download and extract the release ZIP.
2. Double-click **`Setup.bat`**.
3. Setup creates an isolated `.venv`, installs dependencies, downloads/preloads the model, and creates a desktop shortcut.
4. Launch **InSpyCutout** from the shortcut or `Launch_GUI.bat`.

Python 3.11 is used for the environment. If it is not installed and `winget` is available, setup will offer/install it automatically.

The isolated environment is stored in `.venv/`. Persistent app-specific caches are redirected into `cache/` (including the InSPyReNet model, pip cache, and PyTorch-related caches) instead of using your other Python environments.

On NVIDIA systems the setup script installs packages using the official PyTorch CUDA 12.8 wheel index. Other systems use the default/CPU package path.

For reproducibility on Windows, InSpyCutout pins `transparent-background 1.3.4`, `albumentations 1.4.16`, and `albucore 0.0.17`. This avoids newer Albucore/StringZilla builds that may fall back to local C/C++ compilation on some Windows systems.

`Setup.bat` also writes a full `setup.log` next to the app files. If setup fails or the console output scrolls away, attach that file when reporting the problem.

## Controls

| Action | Control |
|---|---|
| Move mode | `M` |
| Paint mode | `B` |
| Swap white / black brush | `X` |
| Brush size | `[` / `]` or GUI slider |
| Undo | `Ctrl+Z` |
| Redo | `Ctrl+Y` / `Ctrl+Shift+Z` |
| Zoom | Mouse wheel |
| Pan | Move mode + left drag |
| Temporary pan | Hold `Space` + left drag |
| Pan anytime | Middle mouse drag |
| Fit image | Double-click |

## Mask meaning

- **White** = keep / opaque
- **Black** = remove / transparent
- **Gray** = partial transparency

## Output

For `sample.png`, InSpyCutout creates:

```text
output/
  sample/
    sample_cutout.png
    sample_mask.png
    sample_raw_mask.png
    sample_edit_mask.png   # only when exported for external editing
```

## Configuration

`config.ini` stores defaults for the model, sliders, paint tool, editor integration, and UI language.

```ini
[ui]
language=auto
paint_preview_ms=90
```

`language=auto` uses Japanese on a Japanese OS and English elsewhere. The GUI language can also be changed with one click and the choice is saved.

### External mask editor

The default is **`Auto Detect (Recommended)`**. When exporting a mask for editing, InSpyCutout tries the following in order:

1. Paint.NET Desktop (registry, PATH, and common install locations)
2. Paint.NET from the Microsoft Store
3. If neither is found, Windows **“Open with…”** is shown

The Microsoft Store build is launched through its Windows app ID instead of a hard-coded installation folder, so it works on other PCs where the same Store app is installed. The classic desktop build is detected separately.

If you prefer Krita, GIMP, or another editor, use **Choose Custom EXE**. The old `Windows default` behavior was removed from the normal choices because PNG files are often associated with a viewer rather than an editor; “Open with…” is a more useful fallback.

## Removing InSpyCutout

Close InSpyCutout, back up anything you want to keep from `output/`, then delete the extracted **InSpyCutout folder**. The app itself, its `.venv`, downloaded model, app-specific caches, settings, and output files are stored under that folder.

Two things can remain outside the folder:

- **Python 3.11**: if Setup installed Python 3.11 for you, Windows keeps it installed because another application may also use it. If you do not use Python 3.11 elsewhere, uninstall it manually later from **Windows Settings > Apps > Installed apps**.
- **Desktop shortcut**: deleting the app folder does not remove a desktop shortcut. Delete it manually if it remains. The default shortcut name is **`InSpyCutout`** (`InSpyCutout.lnk`). If you renamed it, delete the renamed shortcut instead.

No separate uninstaller is required.

## Why this tool?

Automatic background removal is often already 90–99% correct. The frustrating part is fixing a few missed strands, holes, or background remnants. InSpyCutout focuses on that last small correction step instead of trying to become a full image editor.

## Credits

Background removal is powered by [transparent-background](https://github.com/plemeri/transparent-background) and [InSPyReNet](https://github.com/plemeri/InSPyReNet) by their respective authors.

If you use InSPyReNet in academic work, please cite the original ACCV 2022 paper described in the upstream project.

## License

InSpyCutout is released under the [MIT License](LICENSE). See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for dependencies and upstream licenses.
