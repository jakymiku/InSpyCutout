# InSpyCutout

**A lightweight, local, AI-assisted background remover and mask editor for anime / illustration workflows.**

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
- Microsoft Store Paint.NET launch support

## Windows quick start

1. Download and extract the release ZIP.
2. Double-click **`Setup.bat`**.
3. Setup creates an isolated `.venv`, installs dependencies, downloads/preloads the model, and creates a desktop shortcut.
4. Launch **InSpyCutout** from the shortcut or `Launch_GUI.bat`.

Python 3.11 is used for the environment. If it is not installed and `winget` is available, setup will offer/install it automatically.

The isolated environment is stored in `.venv/`. Persistent app-specific caches are redirected into `cache/` (including the InSPyReNet model, pip cache, and PyTorch-related caches) instead of using your other Python environments.

On NVIDIA systems the setup script installs packages using the official PyTorch CUDA 12.8 wheel index. Other systems use the default/CPU package path.

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

## Removing InSpyCutout

Close InSpyCutout, back up anything you want to keep from `output/`, then delete the extracted **InSpyCutout folder**. The app itself, its `.venv`, downloaded model, app-specific caches, settings, and output files are stored under that folder.

Two things can remain outside the folder:

- **Python 3.11**: if Setup installed Python 3.11 for you, Windows keeps it installed because another application may also use it. If you do not use Python 3.11 elsewhere, uninstall it manually later from **Windows Settings > Apps > Installed apps**.
- **Desktop shortcut**: deleting the app folder does not remove a desktop shortcut. Delete it manually if it remains. The default shortcut name is **`InSpyCutout`** (`InSpyCutout.lnk`). If you renamed it, delete the renamed shortcut instead.

No separate uninstaller is required.

## Why this tool?

Automatic background removal is often already 90–99% correct, especially on anime-style images. The frustrating part is fixing a few missed strands, holes, or background remnants. InSpyCutout focuses on that last small correction step instead of trying to become a full image editor.

## Credits

Background removal is powered by [transparent-background](https://github.com/plemeri/transparent-background) and [InSPyReNet](https://github.com/plemeri/InSPyReNet) by their respective authors.

If you use InSPyReNet in academic work, please cite the original ACCV 2022 paper described in the upstream project.

## License

InSpyCutout is released under the [MIT License](LICENSE). See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for dependencies and upstream licenses.
