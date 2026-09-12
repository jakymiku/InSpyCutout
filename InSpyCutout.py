from __future__ import annotations

import argparse
import configparser
import locale
import os
import queue
import shutil
import subprocess
import sys
import threading
from pathlib import Path
from typing import Any

import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageOps, ImageTk


APP_TITLE = "InSpyCutout v0.1.0"

STRINGS = {
    "ja": {
        "open_image": "元画像を選択", "regenerate": "AIマスク再生成", "load_mask": "マスクを読み込む",
        "edit_external": "マスクを書き出して編集", "reload_edit": "編集済みマスク再読込",
        "save": "保存", "open_output": "出力フォルダを開く", "fine_tune": "マスク微調整",
        "gamma_note": "1.00=生マスク / 1未満=半透明部分を濃く残す",
        "offset_note": "+で輪郭を拡張 / -で縮小", "blur_note": "輪郭のぼかし",
        "black_note": "この値以下を完全透明に", "white_note": "この値以上を完全不透明に",
        "reset": "初期値に戻す", "save_settings": "設定を config.ini に保存",
        "editor": "マスク編集アプリ", "custom_exe": "カスタムEXEを選択",
        "paintnet_store": "Paint.NET(Store)に設定", "quick_paint": "簡易マスクペイント",
        "editor_mode_auto": "自動検出 (推奨)", "editor_mode_store": "Paint.NET (Microsoft Store)",
        "editor_mode_desktop": "Paint.NET (デスクトップ版)", "editor_mode_open_with": "Windows「プログラムから開く…」",
        "editor_mode_custom": "カスタムEXE", "detect_paintnet": "Paint.NETを自動検出",
        "operation": "操作:", "move": "移動 (M)", "paint": "ペイント (B)", "brush": "ブラシ:",
        "white_keep": "白(残す)", "black_remove": "黒(消す)", "invert_color": "色反転 (X)",
        "size": "サイズ", "paint_help": "左=選択色 / 右=反対色 / Space押下中=一時移動 / 中ボタンドラッグ=移動",
        "panel_original": "元画像", "panel_mask": "マスク（ここに直接ペイント）", "panel_result": "透過プレビュー",
        "sync_views": "マスク / 透過プレビューの表示を同期",
        "view_sync_on": "マスク / 透過プレビュー同期: ON", "view_sync_off": "マスク / 透過プレビュー同期: OFF",
        "hint_view": "ホイール: 拡大縮小 / 左ドラッグ: 移動 / 中ボタンドラッグ: 移動 / ダブルクリック: フィット",
        "hint_paint": "ペイント: 左=選択色 / 右=反対色 / Space中・中ボタン=移動 / ホイール=ズーム",
        "switch_language": "English", "source": "元画像", "mask": "マスク", "none": "なし",
        "mode_move": "移動", "mode_paint": "ペイント", "mode_status": "操作モード: {mode}",
        "brush_status": "ブラシ: {color} / {size}px", "white": "白", "black": "黒",
        "no_history": "履歴なし", "ready": "準備完了", "loaded": "読み込み: {name}",
        "mask_loaded": "マスク読み込み: {name}", "generating": "InSPyReNetでマスク生成中...",
        "generated": "AIマスク生成完了", "generate_failed": "AIマスク生成失敗",
        "need_image": "先に元画像を選択してください。", "need_image_mask": "先に画像とマスクを準備してください。",
        "need_mask": "先にマスクを生成または読み込んでください。",
        "image_load_failed": "画像の読み込みに失敗しました。\n{error}",
        "mask_load_failed": "マスクの読み込みに失敗しました。\n{error}",
        "mask_size_mismatch": "マスクのサイズが元画像と一致しません。\n\n元画像: {expected_w}×{expected_h}\nマスク: {actual_w}×{actual_h}\n\n誤った位置に適用されるのを防ぐため、サイズを自動変更せず読み込みを中止しました。",
        "ai_failed": "InSPyReNetの実行に失敗しました。\n{error}{hint}",
        "channel_hint": "\n\n画像チャンネル数の不一致が発生しました。RGB入力版を利用してください。",
        "saved": "保存しました。\n\n{path}", "edit_mask_missing": "編集用マスクがありません。\n{path}",
        "editor_failed": "マスクは保存しましたが、エディタを開けませんでした。\n{error}\n\nStore版Paint.NETの場合は『Paint.NET(Store)に設定』を試してください。",
        "settings_saved": "config.ini に現在値を保存しました", "config_missing": "config.ini が見つかりません。\n{path}",
        "choose_image": "元画像を選択", "choose_mask": "マスク画像を選択", "choose_editor": "外部マスク編集アプリを選択",
        "mask_ai": "InSPyReNet", "mask_edited": "編集済み",
        "paintnet_detected_store": "Paint.NET (Microsoft Store) を検出しました。",
        "paintnet_detected_desktop": "Paint.NET を検出しました。\n{path}",
        "paintnet_not_found": "Paint.NET が見つかりませんでした。\nWindowsの「プログラムから開く…」を使用します。",
        "custom_editor_missing": "設定されたカスタムEXEが見つかりません。\nWindowsの「プログラムから開く…」を表示します。\n\n{path}",
        "store_paintnet_missing": "Microsoft Store版 Paint.NET を検出できませんでした。\nWindowsの「プログラムから開く…」を表示します。",
        "desktop_paintnet_missing": "デスクトップ版 Paint.NET を検出できませんでした。\nWindowsの「プログラムから開く…」を表示します。",
    },
    "en": {
        "open_image": "Open Image", "regenerate": "Regenerate AI Mask", "load_mask": "Load Mask",
        "edit_external": "Export Mask to Editor", "reload_edit": "Reload Edited Mask",
        "save": "Save", "open_output": "Open Output Folder", "fine_tune": "Mask Fine Tuning",
        "gamma_note": "1.00 = raw mask / below 1.00 strengthens semi-transparent details",
        "offset_note": "+ expands the edge / - shrinks it", "blur_note": "Edge blur",
        "black_note": "Values at or below this become fully transparent", "white_note": "Values at or above this become fully opaque",
        "reset": "Reset", "save_settings": "Save Settings to config.ini",
        "editor": "Mask Editor", "custom_exe": "Choose Custom EXE",
        "paintnet_store": "Use Paint.NET (Store)", "quick_paint": "Quick Mask Paint",
        "editor_mode_auto": "Auto Detect (Recommended)", "editor_mode_store": "Paint.NET (Microsoft Store)",
        "editor_mode_desktop": "Paint.NET (Desktop)", "editor_mode_open_with": "Windows “Open with…”",
        "editor_mode_custom": "Custom EXE", "detect_paintnet": "Detect Paint.NET",
        "operation": "Mode:", "move": "Move (M)", "paint": "Paint (B)", "brush": "Brush:",
        "white_keep": "White (Keep)", "black_remove": "Black (Remove)", "invert_color": "Swap Color (X)",
        "size": "Size", "paint_help": "Left=selected color / Right=opposite / Hold Space or middle-drag to pan",
        "panel_original": "Original", "panel_mask": "Mask (paint here)", "panel_result": "Transparency Preview",
        "sync_views": "Sync Mask / Transparency Preview view",
        "view_sync_on": "Mask / preview view sync: ON", "view_sync_off": "Mask / preview view sync: OFF",
        "hint_view": "Wheel: zoom / Left-drag: pan / Middle-drag: pan / Double-click: fit",
        "hint_paint": "Paint: Left=selected / Right=opposite / Space or middle-drag=pan / Wheel=zoom",
        "switch_language": "日本語", "source": "Source", "mask": "Mask", "none": "none",
        "mode_move": "Move", "mode_paint": "Paint", "mode_status": "Interaction mode: {mode}",
        "brush_status": "Brush: {color} / {size}px", "white": "white", "black": "black",
        "no_history": "no history", "ready": "Ready", "loaded": "Loaded: {name}",
        "mask_loaded": "Mask loaded: {name}", "generating": "Generating mask with InSPyReNet...",
        "generated": "AI mask generated", "generate_failed": "AI mask generation failed",
        "need_image": "Select an image first.", "need_image_mask": "Prepare an image and mask first.",
        "need_mask": "Generate or load a mask first.",
        "image_load_failed": "Failed to load image.\n{error}", "mask_load_failed": "Failed to load mask.\n{error}",
        "mask_size_mismatch": "The mask size does not match the source image.\n\nSource: {expected_w}×{expected_h}\nMask: {actual_w}×{actual_h}\n\nTo prevent a mask from being applied at the wrong positions, InSpyCutout will not resize it automatically.",
        "ai_failed": "InSPyReNet failed.\n{error}{hint}",
        "channel_hint": "\n\nImage channel mismatch detected. Use the RGB-input build.",
        "saved": "Saved.\n\n{path}", "edit_mask_missing": "Edited mask not found.\n{path}",
        "editor_failed": "The mask was saved, but the editor could not be opened.\n{error}\n\nFor the Microsoft Store version of Paint.NET, choose 'Use Paint.NET (Store)'.",
        "settings_saved": "Saved current values to config.ini", "config_missing": "config.ini was not found.\n{path}",
        "choose_image": "Choose Source Image", "choose_mask": "Choose Mask Image", "choose_editor": "Choose External Mask Editor",
        "mask_ai": "InSPyReNet", "mask_edited": "edited",
        "paintnet_detected_store": "Paint.NET (Microsoft Store) was detected.",
        "paintnet_detected_desktop": "Paint.NET was detected.\n{path}",
        "paintnet_not_found": "Paint.NET was not found.\nWindows “Open with…” will be used.",
        "custom_editor_missing": "The configured custom EXE was not found.\nWindows “Open with…” will be shown.\n\n{path}",
        "store_paintnet_missing": "Paint.NET (Microsoft Store) was not detected.\nWindows “Open with…” will be shown.",
        "desktop_paintnet_missing": "Paint.NET (Desktop) was not detected.\nWindows “Open with…” will be shown.",
    },
}


EDITOR_MODES = ("auto", "paintnet_store", "paintnet_desktop", "windows_open_with", "custom_exe")
EDITOR_MODE_KEYS = {
    "auto": "editor_mode_auto",
    "paintnet_store": "editor_mode_store",
    "paintnet_desktop": "editor_mode_desktop",
    "windows_open_with": "editor_mode_open_with",
    "custom_exe": "editor_mode_custom",
}


def app_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


def configure_local_caches() -> None:
    cache_root = app_dir() / "cache"
    cache_paths = {
        "PIP_CACHE_DIR": cache_root / "pip",
        "TRANSPARENT_BACKGROUND_FILE_PATH": cache_root / "models",
        "TORCH_HOME": cache_root / "torch",
        "TORCH_EXTENSIONS_DIR": cache_root / "torch_extensions",
        "HF_HOME": cache_root / "huggingface",
        "XDG_CACHE_HOME": cache_root / "xdg",
    }
    for key, path in cache_paths.items():
        path.mkdir(parents=True, exist_ok=True)
        os.environ.setdefault(key, str(path))


configure_local_caches()


def load_cfg(path: Path) -> configparser.ConfigParser:
    cfg = configparser.ConfigParser()
    cfg.read(path, encoding="utf-8")
    return cfg


def cfg_get(cfg, section, key, default, cast=None):
    try:
        value = cfg.get(section, key)
        return cast(value) if cast else value
    except Exception:
        return default


def as_bool(value: Any) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "on", "enabled"}


def apply_offset(mask: Image.Image, offset: int) -> Image.Image:
    if offset == 0:
        return mask
    size = abs(offset) * 2 + 1
    return mask.filter(
        ImageFilter.MaxFilter(size=size) if offset > 0 else ImageFilter.MinFilter(size=size)
    )


def apply_thresholds(mask: Image.Image, black: int, white: int) -> Image.Image:
    black = max(0, min(255, int(black)))
    white = max(0, min(255, int(white)))
    if black >= white:
        if black >= 255:
            black = 254
            white = 255
        else:
            white = black + 1

    lut = []
    for i in range(256):
        if i <= black:
            lut.append(0)
        elif i >= white:
            lut.append(255)
        else:
            lut.append(i)
    return mask.point(lut)


def apply_gamma(mask: Image.Image, gamma: float) -> Image.Image:
    gamma = max(0.05, float(gamma))
    if abs(gamma - 1.0) < 1e-9:
        return mask
    lut = [
        max(0, min(255, int(round(((i / 255.0) ** gamma) * 255.0))))
        for i in range(256)
    ]
    return mask.point(lut)


def make_checkerboard(size, cell=16):
    """Create a checkerboard without per-pixel Python loops."""
    w, h = size
    cell = max(2, int(cell))
    c1 = (230, 230, 230)
    c2 = (190, 190, 190)
    bg = Image.new("RGB", (w, h), c1)
    draw = ImageDraw.Draw(bg)
    for y in range(0, h, cell):
        row = y // cell
        for x in range(0, w, cell):
            if ((x // cell) + row) % 2:
                draw.rectangle((x, y, min(w - 1, x + cell - 1), min(h - 1, y + cell - 1)), fill=c2)
    return bg


class ZoomImagePane(ttk.LabelFrame):
    """Zoom/pan preview pane. The mask pane can additionally paint the source mask."""

    def __init__(self, parent, text: str, app=None, editable: bool = False):
        super().__init__(parent, text=text, padding=6)
        self.app = app
        self.editable = editable

        self.canvas = tk.Canvas(self, bg="#202020", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        hint_text = app.tr("hint_paint" if editable else "hint_view") if app else ""
        self.hint = ttk.Label(self, text=hint_text, anchor="center")
        self.hint.pack(fill="x", pady=(4, 0))

        self.base_image: Image.Image | None = None
        self.photo = None
        self.checker = False
        self.fast_render = False
        self.user_scale = 1.0
        self.pan_x = 0.0
        self.pan_y = 0.0
        self._drag_start: tuple[int, int] | None = None
        self._drag_pan_start: tuple[float, float] | None = None
        self._last_size = (1, 1)
        self._drag_mode: str | None = None
        self._paint_button: int | None = None
        self._last_paint_point: tuple[float, float] | None = None
        self._brush_cursor_id = None

        self.canvas.bind("<Configure>", self._on_resize)
        self.canvas.bind("<ButtonPress-1>", self._on_left_press)
        self.canvas.bind("<B1-Motion>", self._on_left_motion)
        self.canvas.bind("<ButtonRelease-1>", self._on_left_release)
        self.canvas.bind("<ButtonPress-2>", self._on_middle_press)
        self.canvas.bind("<B2-Motion>", self._on_middle_motion)
        self.canvas.bind("<ButtonRelease-2>", self._on_middle_release)
        self.canvas.bind("<ButtonPress-3>", self._on_right_press)
        self.canvas.bind("<B3-Motion>", self._on_right_motion)
        self.canvas.bind("<ButtonRelease-3>", self._on_right_release)
        self.canvas.bind("<Double-Button-1>", self._on_double_click)
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        # Windows maps many tilt-wheel / horizontal-scroll events to Shift+MouseWheel.
        # Handle that separately so a slight wheel tilt never changes zoom while panning.
        self.canvas.bind("<Shift-MouseWheel>", self._on_horizontal_wheel)
        self.canvas.bind("<Button-4>", self._on_linux_wheel)
        self.canvas.bind("<Button-5>", self._on_linux_wheel)
        self.canvas.bind("<Motion>", self._on_pointer_motion)
        self.canvas.bind("<Leave>", self._on_pointer_leave)

    def update_language(self):
        if self.app:
            self.hint.configure(text=self.app.tr("hint_paint" if self.editable else "hint_view"))

    def set_image(
        self,
        image: Image.Image | None,
        checker: bool = False,
        reset_view: bool = True,
        fast: bool = False,
    ):
        if image is None:
            self.base_image = None
            self.photo = None
            self.checker = False
            self.canvas.delete("all")
            return

        was_none = self.base_image is None
        # Keep RGBA only when a checkerboard composite is required. The checkerboard
        # itself is generated only for the visible viewport in _draw().
        self.base_image = image.copy().convert("RGBA" if checker else "RGB")
        self.checker = bool(checker)
        self.fast_render = bool(fast)
        if reset_view or was_none:
            self.reset_view(redraw=False)
        self._draw()

    def reset_view(self, redraw: bool = True):
        self.user_scale = 1.0
        self.pan_x = 0.0
        self.pan_y = 0.0
        if redraw:
            self._draw()

    def export_view_state(self):
        """Return absolute zoom plus the image-space point at the canvas center."""
        if self.base_image is None:
            return None
        scale = self._current_scale()
        left, top = self._image_top_left(scale)
        cw = max(1, self.canvas.winfo_width())
        ch = max(1, self.canvas.winfo_height())
        center_x = (cw / 2.0 - left) / scale
        center_y = (ch / 2.0 - top) / scale
        return scale, center_x, center_y

    def import_view_state(self, state, redraw: bool = True):
        """Apply a linked view while keeping the same image-space center and zoom."""
        if self.base_image is None or state is None:
            return
        scale, center_x, center_y = state
        fit = max(0.01, self._fit_scale())
        self.user_scale = max(0.05, min(30.0, float(scale) / fit))
        actual_scale = self._current_scale()
        cw = max(1, self.canvas.winfo_width())
        ch = max(1, self.canvas.winfo_height())
        iw, ih = self.base_image.size
        centered_left = (cw - iw * actual_scale) / 2.0
        centered_top = (ch - ih * actual_scale) / 2.0
        desired_left = cw / 2.0 - float(center_x) * actual_scale
        desired_top = ch / 2.0 - float(center_y) * actual_scale
        self.pan_x = desired_left - centered_left
        self.pan_y = desired_top - centered_top
        if redraw:
            self._draw()

    def _notify_view_changed(self):
        if self.app:
            self.app.sync_linked_view_from(self)

    def _fit_scale(self) -> float:
        if self.base_image is None:
            return 1.0
        cw = max(1, self.canvas.winfo_width())
        ch = max(1, self.canvas.winfo_height())
        iw, ih = self.base_image.size
        return max(0.01, min(cw / max(1, iw), ch / max(1, ih)))

    def _current_scale(self) -> float:
        return max(0.01, min(30.0, self._fit_scale() * self.user_scale))

    def _image_top_left(self, scale: float) -> tuple[float, float]:
        assert self.base_image is not None
        cw = max(1, self.canvas.winfo_width())
        ch = max(1, self.canvas.winfo_height())
        iw, ih = self.base_image.size
        draw_w = iw * scale
        draw_h = ih * scale
        x = (cw - draw_w) / 2 + self.pan_x
        y = (ch - draw_h) / 2 + self.pan_y
        return x, y

    def canvas_to_image(self, x: float, y: float) -> tuple[float, float] | None:
        if self.base_image is None:
            return None
        scale = self._current_scale()
        left, top = self._image_top_left(scale)
        ix = (x - left) / scale
        iy = (y - top) / scale
        iw, ih = self.base_image.size
        if ix < 0 or iy < 0 or ix >= iw or iy >= ih:
            return None
        return ix, iy

    def image_to_canvas(self, x: float, y: float) -> tuple[float, float] | None:
        if self.base_image is None:
            return None
        scale = self._current_scale()
        left, top = self._image_top_left(scale)
        return left + x * scale, top + y * scale

    def _draw(self):
        self.canvas.delete("all")
        self._brush_cursor_id = None
        if self.base_image is None:
            return

        cw = max(1, self.canvas.winfo_width())
        ch = max(1, self.canvas.winfo_height())
        scale = self._current_scale()
        iw, ih = self.base_image.size
        left, top = self._image_top_left(scale)
        right = left + iw * scale
        bottom = top + ih * scale

        # Only render the part of the image that is actually visible in the canvas.
        # v1.4 resized the ENTIRE image at every mouse event; at high zoom this could
        # create huge temporary images and was the main cause of paint stutter.
        vis_l = max(0.0, left)
        vis_t = max(0.0, top)
        vis_r = min(float(cw), right)
        vis_b = min(float(ch), bottom)
        if vis_r <= vis_l or vis_b <= vis_t:
            return

        import math
        ix0 = max(0, int(math.floor((vis_l - left) / scale)))
        iy0 = max(0, int(math.floor((vis_t - top) / scale)))
        ix1 = min(iw, int(math.ceil((vis_r - left) / scale)))
        iy1 = min(ih, int(math.ceil((vis_b - top) / scale)))
        if ix1 <= ix0 or iy1 <= iy0:
            return

        crop = self.base_image.crop((ix0, iy0, ix1, iy1))
        draw_w = max(1, int(round((ix1 - ix0) * scale)))
        draw_h = max(1, int(round((iy1 - iy0) * scale)))

        if self.fast_render:
            resample = Image.Resampling.NEAREST if self.editable else Image.Resampling.BILINEAR
        else:
            resample = Image.Resampling.LANCZOS
        rendered = crop.resize((draw_w, draw_h), resample)

        if self.checker and rendered.mode == "RGBA":
            cell = max(6, min(24, int(round(16 * max(0.5, min(2.0, self.user_scale))))))
            bg = make_checkerboard(rendered.size, cell=cell)
            bg.paste(rendered, (0, 0), rendered)
            rendered = bg
        else:
            rendered = rendered.convert("RGB")

        self.photo = ImageTk.PhotoImage(rendered)
        dest_x = left + ix0 * scale
        dest_y = top + iy0 * scale
        self.canvas.create_image(dest_x, dest_y, image=self.photo, anchor="nw")
        self._update_cursor_style()

    def _update_cursor_style(self):
        if not self.app:
            return
        if self.app.space_down:
            self.canvas.config(cursor="fleur")
        elif self.editable and self.app.interaction_mode.get() == "paint":
            self.canvas.config(cursor="crosshair")
        else:
            self.canvas.config(cursor="fleur")

    def _on_resize(self, _event=None):
        size = (self.canvas.winfo_width(), self.canvas.winfo_height())
        if size != self._last_size:
            self._last_size = size
            self._draw()

    def _start_pan(self, event):
        self._drag_mode = "pan"
        self._drag_start = (event.x, event.y)
        self._drag_pan_start = (self.pan_x, self.pan_y)

    def _pan_move(self, event):
        if self._drag_start is None or self._drag_pan_start is None:
            return
        dx = event.x - self._drag_start[0]
        dy = event.y - self._drag_start[1]
        self.pan_x = self._drag_pan_start[0] + dx
        self.pan_y = self._drag_pan_start[1] + dy
        self._draw()
        self._notify_view_changed()

    def _left_should_pan(self) -> bool:
        if not self.app:
            return True
        if self.app.space_down:
            return True
        if not self.editable:
            return True
        return self.app.interaction_mode.get() == "move"

    def _on_left_press(self, event):
        self.canvas.focus_set()
        if self._left_should_pan():
            self._start_pan(event)
            return
        if self.editable and self.app and self.app.interaction_mode.get() == "paint":
            self._drag_mode = "paint"
            self._paint_button = 1
            self._last_paint_point = None
            self.canvas.delete("paint_overlay")
            self.app.begin_paint_stroke()
            self._paint_at_event(event, button=1)

    def _on_left_motion(self, event):
        if self._drag_mode == "pan":
            self._pan_move(event)
        elif self._drag_mode == "paint":
            self._paint_at_event(event, button=1)
        self._show_brush_cursor(event.x, event.y)

    def _on_left_release(self, _event):
        if self._drag_mode == "paint" and self.app:
            self.app.end_paint_stroke()
        self._drag_mode = None
        self._paint_button = None
        self._last_paint_point = None

    def _on_middle_press(self, event):
        self.canvas.focus_set()
        self._start_pan(event)

    def _on_middle_motion(self, event):
        self._pan_move(event)

    def _on_middle_release(self, _event):
        self._drag_mode = None

    def _on_right_press(self, event):
        self.canvas.focus_set()
        if self.editable and self.app and self.app.interaction_mode.get() == "paint" and not self.app.space_down:
            self._drag_mode = "paint"
            self._paint_button = 3
            self._last_paint_point = None
            self.canvas.delete("paint_overlay")
            self.app.begin_paint_stroke()
            self._paint_at_event(event, button=3)

    def _on_right_motion(self, event):
        if self._drag_mode == "paint":
            self._paint_at_event(event, button=3)
        self._show_brush_cursor(event.x, event.y)

    def _on_right_release(self, _event):
        if self._drag_mode == "paint" and self.app:
            self.app.end_paint_stroke()
        self._drag_mode = None
        self._paint_button = None
        self._last_paint_point = None

    def _paint_at_event(self, event, button: int):
        if not self.app:
            return
        point = self.canvas_to_image(event.x, event.y)
        if point is None:
            self._last_paint_point = None
            return
        previous = self._last_paint_point
        self.app.paint_mask(previous, point, button=button)
        # Immediate canvas-only feedback: this is intentionally separate from the
        # expensive alpha/composite refresh, so the brush follows the pointer smoothly.
        self._draw_paint_overlay(previous, point, button)
        self._last_paint_point = point

    def _draw_paint_overlay(self, start, end, button: int):
        if not self.app or self.base_image is None:
            return
        selected = self.app.brush_color.get()
        color_name = selected if button == 1 else ("black" if selected == "white" else "white")
        fill = "#ffffff" if color_name == "white" else "#000000"
        outline = "#00e5ff" if color_name == "white" else "#ff4d6d"
        size_img = max(1, min(200, int(self.app.brush_size_var.get())))
        width = max(1, int(round(size_img * self._current_scale())))
        exy = self.image_to_canvas(*end)
        if exy is None:
            return
        ex, ey = exy
        if start is None:
            r = max(1, width / 2)
            self.canvas.create_oval(
                ex - r, ey - r, ex + r, ey + r,
                fill=fill, outline=outline, width=1,
                tags=("paint_overlay",),
            )
        else:
            sxy = self.image_to_canvas(*start)
            if sxy is None:
                sxy = exy
            sx, sy = sxy
            self.canvas.create_line(
                sx, sy, ex, ey,
                fill=fill,
                width=width,
                capstyle=tk.ROUND,
                joinstyle=tk.ROUND,
                tags=("paint_overlay",),
            )

    def _on_double_click(self, _event=None):
        # In Paint mode, a double-click is still a paint action. Do not unexpectedly
        # reset/fit the mask view after the first click has already painted a stroke.
        if self.editable and self.app and self.app.interaction_mode.get() == "paint" and not self.app.space_down:
            return "break"
        if self._drag_mode == "paint":
            return "break"
        self.reset_view()
        self._notify_view_changed()
        return "break"

    def _zoom_at(self, x: float, y: float, zoom_factor: float):
        if self.base_image is None:
            return
        old_scale = self._current_scale()
        new_user_scale = max(0.05, min(30.0, self.user_scale * zoom_factor))
        if abs(new_user_scale - self.user_scale) < 1e-9:
            return

        old_top_x, old_top_y = self._image_top_left(old_scale)
        img_x = (x - old_top_x) / old_scale
        img_y = (y - old_top_y) / old_scale

        self.user_scale = new_user_scale
        new_scale = self._current_scale()
        cw = max(1, self.canvas.winfo_width())
        ch = max(1, self.canvas.winfo_height())
        iw, ih = self.base_image.size
        centered_left = (cw - iw * new_scale) / 2
        centered_top = (ch - ih * new_scale) / 2
        self.pan_x = x - img_x * new_scale - centered_left
        self.pan_y = y - img_y * new_scale - centered_top
        self._draw()
        self._notify_view_changed()

    def _on_mousewheel(self, event):
        # Do not zoom while the user is actively panning. This also prevents
        # accidental tilt-wheel events from fighting middle-button dragging.
        if self._drag_mode == "pan":
            return "break"

        # Some Windows mouse drivers report wheel tilt as Shift+MouseWheel.
        # Ignore horizontal wheel input here; vertical wheel remains zoom-only.
        if getattr(event, "state", 0) & 0x0001:
            return "break"

        if not getattr(event, "delta", 0):
            return "break"
        factor = 1.1 if event.delta > 0 else 1 / 1.1
        self._zoom_at(event.x, event.y, factor)
        self._show_brush_cursor(event.x, event.y)
        return "break"

    def _on_horizontal_wheel(self, _event):
        # Intentionally ignore left/right wheel tilt. Pan remains controlled by
        # left-drag in Move mode, Space+left-drag, or middle-button drag.
        return "break"

    def _on_linux_wheel(self, event):
        factor = 1.1 if event.num == 4 else 1 / 1.1
        self._zoom_at(event.x, event.y, factor)
        self._show_brush_cursor(event.x, event.y)

    def _on_pointer_motion(self, event):
        self._show_brush_cursor(event.x, event.y)

    def _on_pointer_leave(self, _event):
        if self._brush_cursor_id is not None:
            try:
                self.canvas.delete(self._brush_cursor_id)
            except Exception:
                pass
            self._brush_cursor_id = None

    def _show_brush_cursor(self, x: int, y: int):
        if not (self.editable and self.app):
            return
        if self.app.interaction_mode.get() != "paint" or self.app.space_down:
            if self._brush_cursor_id is not None:
                self.canvas.delete(self._brush_cursor_id)
                self._brush_cursor_id = None
            self._update_cursor_style()
            return
        self._update_cursor_style()
        if self.base_image is None or self.canvas_to_image(x, y) is None:
            if self._brush_cursor_id is not None:
                self.canvas.delete(self._brush_cursor_id)
                self._brush_cursor_id = None
            return
        radius = max(1.0, float(self.app.brush_size_var.get()) * self._current_scale() / 2.0)
        color = "white" if self.app.brush_color.get() == "white" else "black"
        outline = "#00e5ff" if color == "white" else "#ff4d6d"
        if self._brush_cursor_id is not None:
            self.canvas.delete(self._brush_cursor_id)
        self._brush_cursor_id = self.canvas.create_oval(
            x - radius,
            y - radius,
            x + radius,
            y + radius,
            outline=outline,
            width=2,
        )


class App(tk.Tk):
    def __init__(self, cfg_path: Path, initial_image: str | None = None):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("1580x960")
        self.minsize(1180, 720)

        self.cfg_path = cfg_path
        self.cfg = load_cfg(cfg_path)
        self.base_dir = app_dir()
        self.output_root = self.base_dir / "output"
        self.output_root.mkdir(parents=True, exist_ok=True)

        lang_cfg = cfg_get(self.cfg, "ui", "language", "auto").strip().lower()
        if lang_cfg not in {"ja", "en"}:
            system_lang = (locale.getlocale()[0] or "").lower()
            lang_cfg = "ja" if system_lang.startswith("ja") else "en"
        self.language = lang_cfg
        self._i18n_widgets = []

        self.source_path: Path | None = None
        self.source_rgba: Image.Image | None = None
        self.raw_mask: Image.Image | None = None
        self.processed_mask: Image.Image | None = None
        self.result_rgba: Image.Image | None = None
        self.mask_source_kind = "none"
        self.mask_source_detail: str | None = None
        self.mask_source_label = tk.StringVar(value=f"{self.tr('mask')}: {self.tr('none')}")
        self.status = tk.StringVar(value=self.tr("ready"))
        self.remover = None
        self.worker_queue: queue.Queue = queue.Queue()
        self._preview_after = None
        self._paint_preview_after = None
        self._syncing_threshold = False
        self.space_down = False
        self.undo_stack: list[Image.Image] = []
        self.redo_stack: list[Image.Image] = []
        self._stroke_before: Image.Image | None = None
        self._stroke_dirty = False
        self._painting_active = False
        self.paint_preview_ms = max(50, cfg_get(self.cfg, "ui", "paint_preview_ms", 90, int))
        self.sync_mask_preview = tk.BooleanVar(
            value=as_bool(cfg_get(self.cfg, "ui", "sync_mask_preview", "1"))
        )
        self.max_history = 20

        self.gamma_var = tk.DoubleVar(value=cfg_get(self.cfg, "defaults", "alpha_gamma", 0.72, float))
        self.offset_var = tk.IntVar(value=cfg_get(self.cfg, "defaults", "mask_offset", 0, int))
        self.blur_var = tk.DoubleVar(value=cfg_get(self.cfg, "defaults", "mask_blur", 0.0, float))
        self.black_var = tk.IntVar(value=cfg_get(self.cfg, "defaults", "black_threshold", 0, int))
        self.white_var = tk.IntVar(value=cfg_get(self.cfg, "defaults", "white_threshold", 250, int))
        self.interaction_mode = tk.StringVar(value=cfg_get(self.cfg, "paint", "mode", "move"))
        self.brush_color = tk.StringVar(value=cfg_get(self.cfg, "paint", "brush_color", "white"))
        self.brush_size_var = tk.IntVar(value=cfg_get(self.cfg, "paint", "brush_size", 32, int))
        editor_mode = cfg_get(self.cfg, "editor", "mode", "auto").strip()
        if editor_mode == "windows_default":
            editor_mode = "windows_open_with"
        if editor_mode not in EDITOR_MODES:
            editor_mode = "auto"
        self.editor_mode = tk.StringVar(value=editor_mode)
        self.editor_display = tk.StringVar()
        self.paintnet_aumid = cfg_get(
            self.cfg,
            "editor",
            "paintnet_aumid",
            "dotPDNLLC.paint.net_h55e3w7q8jbva!dotPDNLLC.paint.net",
        )
        self.paintnet_desktop_path = cfg_get(self.cfg, "editor", "paintnet_desktop_path", "").strip().strip('"')

        self._build_ui()
        self._setup_var_traces()
        self._setup_shortcuts()
        self.after(100, self._poll_worker)

        if initial_image:
            p = Path(initial_image)
            if p.exists():
                self.after(200, lambda: self.load_source(p, auto_generate=True))

    def tr(self, key: str, **kwargs):
        text = STRINGS.get(self.language, STRINGS["en"]).get(key, key)
        return text.format(**kwargs) if kwargs else text

    def _iw(self, widget, key: str):
        self._i18n_widgets.append((widget, key))
        try:
            widget.configure(text=self.tr(key))
        except Exception:
            pass
        return widget

    def _set_mask_source(self, kind: str, detail: str | None = None):
        self.mask_source_kind = kind
        self.mask_source_detail = detail
        self._refresh_mask_source_label()

    def _refresh_mask_source_label(self):
        kind = getattr(self, "mask_source_kind", "none")
        detail = getattr(self, "mask_source_detail", None)
        if kind == "ai":
            value = self.tr("mask_ai")
        elif kind == "edited":
            value = self.tr("mask_edited")
            if detail:
                value += f" ({detail})"
        elif kind == "file":
            value = detail or self.tr("none")
        else:
            value = self.tr("none")
        self.mask_source_label.set(f"{self.tr('mask')}: {value}")

    def _editor_mode_label(self, mode: str | None = None) -> str:
        mode = mode or self.editor_mode.get()
        return self.tr(EDITOR_MODE_KEYS.get(mode, "editor_mode_auto"))

    def _refresh_editor_combo(self):
        combo = getattr(self, "editor_combo", None)
        if combo is None:
            return
        labels = [self.tr(EDITOR_MODE_KEYS[m]) for m in EDITOR_MODES]
        combo.configure(values=labels)
        self.editor_display.set(self._editor_mode_label())

    def _on_editor_combo_selected(self, _event=None):
        selected = self.editor_display.get()
        for mode in EDITOR_MODES:
            if selected == self.tr(EDITOR_MODE_KEYS[mode]):
                self.editor_mode.set(mode)
                break
        self.save_editor_mode()

    def toggle_language(self):
        self.language = "en" if self.language == "ja" else "ja"
        if not self.cfg.has_section("ui"):
            self.cfg.add_section("ui")
        self.cfg["ui"]["language"] = self.language
        self._write_cfg()
        self.apply_language()

    def apply_language(self):
        for widget, key in self._i18n_widgets:
            try:
                widget.configure(text=self.tr(key))
            except Exception:
                pass
        self.language_button.configure(text=self.tr("switch_language"))
        for pane in (getattr(self, "original_panel", None), getattr(self, "mask_panel", None), getattr(self, "result_panel", None)):
            if pane:
                pane.update_language()
        if getattr(self, "original_panel", None):
            self.original_panel.configure(text=self.tr("panel_original"))
            self.mask_panel.configure(text=self.tr("panel_mask"))
            self.result_panel.configure(text=self.tr("panel_result"))
        if self.source_path:
            self.path_label.configure(text=f"{self.tr('source')}: {self.source_path}")
        else:
            self.path_label.configure(text=f"{self.tr('source')}: {self.tr('none')}")
        self._refresh_mask_source_label()
        self._refresh_editor_combo()

        # The bottom-left status text is not a widget registered through _iw().
        # If the most recent status came from the view-sync toggle, translate that
        # transient message too when switching UI languages.
        current_status = self.status.get()
        for key in ("view_sync_on", "view_sync_off"):
            known = {
                STRINGS.get("ja", {}).get(key, ""),
                STRINGS.get("en", {}).get(key, ""),
            }
            if current_status in known:
                self.status.set(self.tr(key))
                break

    def _build_ui(self):
        top = ttk.Frame(self, padding=8)
        top.pack(fill="x")

        for key, command, padx in [
            ("open_image", self.choose_source, 4), ("regenerate", self.generate_ai_mask, 4),
            ("load_mask", self.choose_mask, 4), ("edit_external", self.export_mask_for_edit, 4),
            ("reload_edit", self.reload_edit_mask, 4), ("save", self.save_all, 14),
            ("open_output", self.open_output_folder, 4),
        ]:
            self._iw(ttk.Button(top, command=command), key).pack(side="left", padx=padx)
        self.language_button = ttk.Button(top, text=self.tr("switch_language"), command=self.toggle_language)
        self.language_button.pack(side="right", padx=4)

        path_row = ttk.Frame(self, padding=(8, 0, 8, 4))
        path_row.pack(fill="x")
        self.path_label = ttk.Label(path_row, text=f"{self.tr('source')}: {self.tr('none')}")
        self.path_label.pack(side="left", fill="x", expand=True)
        ttk.Label(path_row, textvariable=self.mask_source_label).pack(side="right")

        controls = self._iw(ttk.LabelFrame(self, padding=8), "fine_tune")
        controls.pack(fill="x", padx=8, pady=4)
        self._add_scale(controls, "Alpha Gamma", self.gamma_var, 0.30, 1.50, 0.01, 0, "gamma_note", "float2")
        self._add_scale(controls, "Mask Offset", self.offset_var, -5, 5, 1, 1, "offset_note", "int")
        self._add_scale(controls, "Mask Blur", self.blur_var, 0.0, 5.0, 0.1, 2, "blur_note", "float1")
        self._add_scale(controls, "Black Threshold", self.black_var, 0, 255, 1, 3, "black_note", "int")
        self._add_scale(controls, "White Threshold", self.white_var, 0, 255, 1, 4, "white_note", "int")

        side = ttk.Frame(controls)
        side.grid(row=0, column=5, rowspan=5, sticky="ns", padx=(18, 0))
        self._iw(ttk.Button(side, command=self.reset_sliders), "reset").pack(fill="x", pady=3)
        self._iw(ttk.Button(side, command=self.save_settings), "save_settings").pack(fill="x", pady=3)
        self._iw(ttk.Label(side), "editor").pack(anchor="w", pady=(10, 2))
        self.editor_combo = ttk.Combobox(side, textvariable=self.editor_display, state="readonly", width=26)
        self.editor_combo.pack(fill="x", pady=2)
        self.editor_combo.bind("<<ComboboxSelected>>", self._on_editor_combo_selected)
        self._refresh_editor_combo()
        self._iw(ttk.Button(side, command=self.choose_editor), "custom_exe").pack(fill="x", pady=3)
        self._iw(ttk.Button(side, command=self.detect_paintnet), "detect_paintnet").pack(fill="x", pady=3)

        paintbar = self._iw(ttk.LabelFrame(self, padding=(8, 5)), "quick_paint")
        paintbar.pack(fill="x", padx=8, pady=(2, 4))
        self._iw(ttk.Label(paintbar), "operation").pack(side="left", padx=(0, 4))
        self._iw(ttk.Radiobutton(paintbar, value="move", variable=self.interaction_mode, command=self.on_mode_changed), "move").pack(side="left", padx=3)
        self._iw(ttk.Radiobutton(paintbar, value="paint", variable=self.interaction_mode, command=self.on_mode_changed), "paint").pack(side="left", padx=3)
        ttk.Separator(paintbar, orient="vertical").pack(side="left", fill="y", padx=10)
        self._iw(ttk.Label(paintbar), "brush").pack(side="left")
        self._iw(ttk.Radiobutton(paintbar, value="white", variable=self.brush_color, command=self.on_brush_changed), "white_keep").pack(side="left", padx=3)
        self._iw(ttk.Radiobutton(paintbar, value="black", variable=self.brush_color, command=self.on_brush_changed), "black_remove").pack(side="left", padx=3)
        self._iw(ttk.Button(paintbar, command=self.swap_brush_color), "invert_color").pack(side="left", padx=5)
        self._iw(ttk.Label(paintbar), "size").pack(side="left", padx=(12, 3))
        tk.Scale(paintbar, from_=1, to=200, resolution=1, orient="horizontal", variable=self.brush_size_var, length=220).pack(side="left")
        ttk.Spinbox(paintbar, from_=1, to=200, increment=1, textvariable=self.brush_size_var, width=6).pack(side="left", padx=3)
        ttk.Separator(paintbar, orient="vertical").pack(side="left", fill="y", padx=10)
        ttk.Button(paintbar, text="Undo (Ctrl+Z)", command=self.undo_paint).pack(side="left", padx=3)
        ttk.Button(paintbar, text="Redo (Ctrl+Y)", command=self.redo_paint).pack(side="left", padx=3)
        self._iw(ttk.Label(paintbar), "paint_help").pack(side="left", padx=(12, 0))

        viewbar = ttk.Frame(self, padding=(12, 0, 12, 0))
        viewbar.pack(fill="x")
        self._iw(
            ttk.Checkbutton(
                viewbar,
                variable=self.sync_mask_preview,
                command=self.on_view_sync_changed,
            ),
            "sync_views",
        ).pack(side="right")

        previews = ttk.Frame(self, padding=8)
        previews.pack(fill="both", expand=True)
        for col in range(3): previews.columnconfigure(col, weight=1)
        previews.rowconfigure(0, weight=1)
        self.original_panel = ZoomImagePane(previews, self.tr("panel_original"), app=self, editable=False)
        self.original_panel.grid(row=0, column=0, sticky="nsew", padx=4)
        self.mask_panel = ZoomImagePane(previews, self.tr("panel_mask"), app=self, editable=True)
        self.mask_panel.grid(row=0, column=1, sticky="nsew", padx=4)
        self.result_panel = ZoomImagePane(previews, self.tr("panel_result"), app=self, editable=False)
        self.result_panel.grid(row=0, column=2, sticky="nsew", padx=4)

        bottom = ttk.Frame(self, padding=8)
        bottom.pack(fill="x")
        ttk.Label(bottom, textvariable=self.status).pack(side="left")
        self.progress = ttk.Progressbar(bottom, mode="indeterminate", length=240)
        self.progress.pack(side="right")

    def _add_scale(self, parent, label, var, frm, to, resolution, row, note_key, spin_format="int"):
        ttk.Label(parent, text=label, width=17).grid(row=row, column=0, sticky="w")
        scale = tk.Scale(parent, from_=frm, to=to, resolution=resolution, orient="horizontal", variable=var, length=360, command=lambda _=None: self.schedule_reprocess())
        scale.grid(row=row, column=1, sticky="ew", padx=5)
        if spin_format == "int":
            spin = ttk.Spinbox(parent, from_=frm, to=to, increment=resolution, textvariable=var, width=8)
        else:
            spin = ttk.Spinbox(parent, from_=frm, to=to, increment=resolution, textvariable=var, width=8, format="%.2f")
        spin.grid(row=row, column=2, padx=(4, 2))
        for event in ("<KeyRelease>", "<FocusOut>", "<<Increment>>", "<<Decrement>>"):
            spin.bind(event, lambda _e: self.schedule_reprocess())
        self._iw(ttk.Label(parent), note_key).grid(row=row, column=3, sticky="w", padx=10)
        parent.columnconfigure(1, weight=1)

    def _setup_var_traces(self):
        self.black_var.trace_add("write", lambda *_: self._on_black_changed())
        self.white_var.trace_add("write", lambda *_: self._on_white_changed())
        self.brush_size_var.trace_add("write", lambda *_: self.on_brush_changed())

    def _setup_shortcuts(self):
        self.bind_all("<KeyPress-space>", self._space_press)
        self.bind_all("<KeyRelease-space>", self._space_release)
        self.bind_all("<Control-z>", lambda _e: self.undo_paint())
        self.bind_all("<Control-y>", lambda _e: self.redo_paint())
        self.bind_all("<Control-Shift-Z>", lambda _e: self.redo_paint())
        self.bind_all("<KeyPress-m>", lambda _e: self.set_interaction_mode("move"))
        self.bind_all("<KeyPress-M>", lambda _e: self.set_interaction_mode("move"))
        self.bind_all("<KeyPress-b>", lambda _e: self.set_interaction_mode("paint"))
        self.bind_all("<KeyPress-B>", lambda _e: self.set_interaction_mode("paint"))
        self.bind_all("<KeyPress-x>", lambda _e: self.swap_brush_color())
        self.bind_all("<KeyPress-X>", lambda _e: self.swap_brush_color())
        self.bind_all("<KeyPress-bracketleft>", lambda _e: self.adjust_brush_size(-4))
        self.bind_all("<KeyPress-bracketright>", lambda _e: self.adjust_brush_size(4))

    def _space_press(self, _event=None):
        if not self.space_down:
            self.space_down = True
            self._refresh_pane_cursors()

    def _space_release(self, _event=None):
        if self.space_down:
            self.space_down = False
            self._refresh_pane_cursors()

    def _refresh_pane_cursors(self):
        for pane_name in ("original_panel", "mask_panel", "result_panel"):
            pane = getattr(self, pane_name, None)
            if pane:
                pane._update_cursor_style()

    def sync_linked_view_from(self, source_pane):
        """Keep the mask and transparency preview on the same image region when enabled."""
        if not self.sync_mask_preview.get():
            return
        mask = getattr(self, "mask_panel", None)
        result = getattr(self, "result_panel", None)
        if source_pane is mask:
            target = result
        elif source_pane is result:
            target = mask
        else:
            return
        if target is None or source_pane.base_image is None or target.base_image is None:
            return
        target.import_view_state(source_pane.export_view_state())

    def on_view_sync_changed(self):
        enabled = bool(self.sync_mask_preview.get())
        if enabled:
            # When sync is enabled, make the transparency preview immediately match
            # the mask view (or the reverse if only the result currently has an image).
            source = self.mask_panel if self.mask_panel.base_image is not None else self.result_panel
            self.sync_linked_view_from(source)
        if not self.cfg.has_section("ui"):
            self.cfg.add_section("ui")
        self.cfg["ui"]["sync_mask_preview"] = "1" if enabled else "0"
        self._write_cfg()
        self.status.set(self.tr("view_sync_on" if enabled else "view_sync_off"))

    def set_interaction_mode(self, mode: str):
        if mode not in {"move", "paint"}:
            return
        self.interaction_mode.set(mode)
        self.on_mode_changed()

    def on_mode_changed(self):
        self._refresh_pane_cursors()
        label = self.tr("mode_move") if self.interaction_mode.get() == "move" else self.tr("mode_paint")
        self.status.set(self.tr("mode_status", mode=label))

    def on_brush_changed(self):
        try:
            size = max(1, min(200, int(self.brush_size_var.get())))
            if size != self.brush_size_var.get():
                self.brush_size_var.set(size)
        except Exception:
            return
        color = self.tr("white" if self.brush_color.get() == "white" else "black")
        self.status.set(self.tr("brush_status", color=color, size=size))

    def swap_brush_color(self):
        self.brush_color.set("black" if self.brush_color.get() == "white" else "white")
        self.on_brush_changed()

    def adjust_brush_size(self, delta: int):
        try:
            self.brush_size_var.set(max(1, min(200, int(self.brush_size_var.get()) + delta)))
        except Exception:
            pass

    def begin_paint_stroke(self):
        if self.raw_mask is None:
            return
        self._painting_active = True
        self._stroke_dirty = False
        self._stroke_before = self.raw_mask.copy()

    def end_paint_stroke(self):
        if self.raw_mask is None or self._stroke_before is None:
            self._stroke_before = None
            self._painting_active = False
            return
        # Keep one undo step per drag stroke without scanning the full image with tobytes().
        if self._stroke_dirty:
            self.undo_stack.append(self._stroke_before)
            if len(self.undo_stack) > self.max_history:
                self.undo_stack.pop(0)
            self.redo_stack.clear()
        self._stroke_before = None
        self._stroke_dirty = False
        self._painting_active = False

        if self._paint_preview_after is not None:
            try:
                self.after_cancel(self._paint_preview_after)
            except Exception:
                pass
            self._paint_preview_after = None

        # Mouse-up is the quality boundary: redraw once with LANCZOS/full-quality data.
        self.after_idle(lambda: self.reprocess_preview(live_paint=False))

    def paint_mask(self, start, end, button: int = 1):
        if self.raw_mask is None:
            return
        selected = self.brush_color.get()
        color_name = selected if button == 1 else ("black" if selected == "white" else "white")
        value = 255 if color_name == "white" else 0
        size = max(1, min(200, int(self.brush_size_var.get())))
        radius = size / 2.0

        draw = ImageDraw.Draw(self.raw_mask)
        ex, ey = end
        if start is None:
            draw.ellipse((ex - radius, ey - radius, ex + radius, ey + radius), fill=value)
        else:
            sx, sy = start
            draw.line((sx, sy, ex, ey), fill=value, width=size)
            draw.ellipse((sx - radius, sy - radius, sx + radius, sy + radius), fill=value)
            draw.ellipse((ex - radius, ey - radius, ex + radius, ey + radius), fill=value)

        self._stroke_dirty = True
        self.schedule_paint_preview()

    def schedule_paint_preview(self):
        # Brush feedback itself is drawn instantly on the mask canvas. The alpha preview
        # is deliberately throttled so Tk/Pillow do not fight the mouse event loop.
        if self._paint_preview_after is None:
            self._paint_preview_after = self.after(self.paint_preview_ms, self._paint_preview_tick)

    def _paint_preview_tick(self):
        self._paint_preview_after = None
        if not self._painting_active:
            return
        self.reprocess_preview(live_paint=True)

    def undo_paint(self):
        if self.raw_mask is None or not self.undo_stack:
            self.status.set(f"Undo: {self.tr('no_history')}")
            return
        self.redo_stack.append(self.raw_mask.copy())
        self.raw_mask = self.undo_stack.pop()
        self.reprocess_preview(live_paint=False)
        self.status.set("Undo")

    def redo_paint(self):
        if self.raw_mask is None or not self.redo_stack:
            self.status.set(f"Redo: {self.tr('no_history')}")
            return
        self.undo_stack.append(self.raw_mask.copy())
        self.raw_mask = self.redo_stack.pop()
        self.reprocess_preview(live_paint=False)
        self.status.set("Redo")

    def _reset_history(self):
        self.undo_stack.clear()
        self.redo_stack.clear()
        self._stroke_before = None
        self._stroke_dirty = False
        self._painting_active = False

    def _clamp_int_var(self, var: tk.IntVar, lo: int, hi: int):
        try:
            value = int(var.get())
        except Exception:
            value = lo
        value = max(lo, min(hi, value))
        try:
            current = int(var.get())
        except Exception:
            current = None
        if value != current:
            var.set(value)
        return value

    def _on_black_changed(self):
        if self._syncing_threshold:
            return
        self._syncing_threshold = True
        try:
            black = self._clamp_int_var(self.black_var, 0, 255)
            white = self._clamp_int_var(self.white_var, 0, 255)
            if black >= white:
                if black >= 255:
                    self.black_var.set(254)
                    self.white_var.set(255)
                else:
                    self.white_var.set(black + 1)
        finally:
            self._syncing_threshold = False
        self.schedule_reprocess()

    def _on_white_changed(self):
        if self._syncing_threshold:
            return
        self._syncing_threshold = True
        try:
            black = self._clamp_int_var(self.black_var, 0, 255)
            white = self._clamp_int_var(self.white_var, 0, 255)
            if white <= black:
                if white <= 0:
                    self.white_var.set(1)
                    self.black_var.set(0)
                else:
                    self.black_var.set(white - 1)
        finally:
            self._syncing_threshold = False
        self.schedule_reprocess()

    def choose_source(self):
        path = filedialog.askopenfilename(
            title=self.tr("choose_image"),
            filetypes=[("Image", "*.png *.jpg *.jpeg *.webp *.bmp *.tif *.tiff"), ("All files", "*.*")],
        )
        if path:
            self.load_source(Path(path), auto_generate=True)

    def load_source(self, path: Path, auto_generate=True):
        try:
            self.source_path = path
            # Apply EXIF orientation before converting to RGBA. Smartphone/camera images
            # often store pixels sideways and rely on EXIF Orientation for display.
            with Image.open(path) as opened:
                self.source_rgba = ImageOps.exif_transpose(opened).convert("RGBA")
            self.raw_mask = None
            self.processed_mask = None
            self.result_rgba = None
            self._reset_history()
            self._set_mask_source("none")
            self.path_label.config(text=f"{self.tr('source')}: {path}")
            self.status.set(self.tr("loaded", name=path.name))
            self._show_original()
            self.mask_panel.set_image(None)
            self.result_panel.set_image(None)
            if auto_generate:
                self.generate_ai_mask()
        except Exception as e:
            messagebox.showerror(APP_TITLE, self.tr("image_load_failed", error=e))

    def choose_mask(self):
        if not self.source_rgba:
            messagebox.showinfo(APP_TITLE, self.tr("need_image"))
            return
        path = filedialog.askopenfilename(
            title=self.tr("choose_mask"),
            filetypes=[("Image", "*.png *.jpg *.jpeg *.webp *.bmp"), ("All files", "*.*")],
        )
        if path:
            self.load_mask(Path(path), source_kind="file")

    def load_mask(self, path: Path, source_kind="file"):
        try:
            with Image.open(path) as opened:
                mask = ImageOps.exif_transpose(opened).convert("L")
            if mask.size != self.source_rgba.size:
                expected_w, expected_h = self.source_rgba.size
                actual_w, actual_h = mask.size
                messagebox.showerror(
                    APP_TITLE,
                    self.tr(
                        "mask_size_mismatch",
                        expected_w=expected_w,
                        expected_h=expected_h,
                        actual_w=actual_w,
                        actual_h=actual_h,
                    ),
                )
                self.status.set(
                    f"Mask size mismatch: {actual_w}x{actual_h} != {expected_w}x{expected_h}"
                )
                return
            self.raw_mask = mask
            self._reset_history()
            self._set_mask_source(source_kind, path.name)
            self.status.set(self.tr("mask_loaded", name=path.name))
            self.reprocess_preview()
        except Exception as e:
            messagebox.showerror(APP_TITLE, self.tr("mask_load_failed", error=e))

    def _make_remover(self):
        if self.remover is not None:
            return self.remover
        from transparent_background import Remover

        mode = cfg_get(self.cfg, "inspy", "mode", "base")
        device = cfg_get(self.cfg, "inspy", "device", "auto").strip().lower()
        jit = as_bool(cfg_get(self.cfg, "inspy", "torchscript", "0"))
        resize = cfg_get(self.cfg, "inspy", "resize", "static")
        if device == "auto":
            try:
                import torch
                if torch.cuda.is_available():
                    device = "cuda:0"
                elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
                    device = "mps"
                else:
                    device = "cpu"
            except Exception:
                device = "cpu"
        try:
            self.remover = Remover(mode=mode, device=device, jit=jit, resize=resize)
        except TypeError:
            try:
                self.remover = Remover(mode=mode, device=device, jit=jit)
            except TypeError:
                try:
                    self.remover = Remover(mode=mode, jit=jit)
                except TypeError:
                    self.remover = Remover()
        return self.remover

    def generate_ai_mask(self):
        if not self.source_rgba or not self.source_path:
            messagebox.showinfo(APP_TITLE, self.tr("need_image"))
            return

        self.status.set(self.tr("generating"))
        self.progress.start(10)
        source = self.source_rgba.convert("RGB")

        def worker():
            try:
                remover = self._make_remover()
                result = remover.process(source, type="rgba")
                if isinstance(result, Image.Image):
                    rgba = result.convert("RGBA")
                else:
                    try:
                        import numpy as np

                        arr = np.asarray(result)
                        if arr.dtype != np.uint8:
                            if arr.max() <= 1.0:
                                arr = (arr * 255.0).clip(0, 255).astype(np.uint8)
                            else:
                                arr = arr.clip(0, 255).astype(np.uint8)
                        rgba = Image.fromarray(arr).convert("RGBA")
                    except Exception as exc:
                        raise RuntimeError(f"Unsupported result type: {type(result)!r}") from exc

                if rgba.size != source.size:
                    rgba = rgba.resize(source.size, Image.Resampling.LANCZOS)
                raw = rgba.getchannel("A")
                self.worker_queue.put(("mask", raw))
            except Exception as e:
                self.worker_queue.put(("error", str(e)))

        threading.Thread(target=worker, daemon=True).start()

    def _poll_worker(self):
        try:
            while True:
                kind, payload = self.worker_queue.get_nowait()
                if kind == "mask":
                    self.progress.stop()
                    self.raw_mask = payload
                    self._reset_history()
                    self._set_mask_source("ai")
                    self.status.set(self.tr("generated"))
                    self.reprocess_preview()
                elif kind == "error":
                    self.progress.stop()
                    self.status.set(self.tr("generate_failed"))
                    hint = ""
                    if "could not be broadcast together" in payload:
                        hint = self.tr("channel_hint")
                    messagebox.showerror(APP_TITLE, self.tr("ai_failed", error=payload, hint=hint))
        except queue.Empty:
            pass
        self.after(100, self._poll_worker)

    def schedule_reprocess(self):
        if self._preview_after is not None:
            try:
                self.after_cancel(self._preview_after)
            except Exception:
                pass
        self._preview_after = self.after(80, self.reprocess_preview)

    def reprocess_preview(self, live_paint: bool = False):
        self._preview_after = None
        if self.raw_mask is None or self.source_rgba is None:
            return

        mask = self.raw_mask.copy().convert("L")
        offset = int(self.offset_var.get())
        blur = float(self.blur_var.get())
        black = int(self.black_var.get())
        white = int(self.white_var.get())
        gamma = float(self.gamma_var.get())

        if offset != 0:
            mask = apply_offset(mask, offset)
        if blur > 0:
            mask = mask.filter(ImageFilter.GaussianBlur(radius=blur))
        mask = apply_thresholds(mask, black, white)
        mask = apply_gamma(mask, gamma)

        # Never make pixels more opaque than they were in the source image. This
        # preserves pre-existing PNG/WebP transparency even if the AI/manual mask
        # paints those pixels white. For ordinary JPEG/RGB images source alpha is 255,
        # so this is a no-op.
        source_alpha = self.source_rgba.getchannel("A")
        final_alpha = ImageChops.darker(mask, source_alpha)

        self.processed_mask = final_alpha
        result = self.source_rgba.copy()
        result.putalpha(final_alpha)
        self.result_rgba = result

        self.mask_panel.set_image(
            final_alpha.convert("RGB"), checker=False, reset_view=False, fast=live_paint
        )
        self.result_panel.set_image(
            result, checker=True, reset_view=False, fast=live_paint
        )

        self.status.set(
            f"Preview: gamma={gamma:.2f} offset={offset} blur={blur:.1f} black={black} white={white}"
        )

    def _show_original(self):
        if self.source_rgba:
            # Show a checkerboard for source images that already contain transparency.
            # Fully opaque images keep the normal preview.
            alpha_min, _alpha_max = self.source_rgba.getchannel("A").getextrema()
            self.original_panel.set_image(self.source_rgba, checker=(alpha_min < 255))

    def current_output_dir(self) -> Path | None:
        if not self.source_path:
            return None
        out = self.output_root / self.source_path.stem
        out.mkdir(parents=True, exist_ok=True)
        return out

    def save_all(self):
        if self.result_rgba is None or self.processed_mask is None or not self.source_path:
            messagebox.showinfo(APP_TITLE, self.tr("need_image_mask"))
            return

        out = self.current_output_dir()
        cutout = out / f"{self.source_path.stem}_cutout.png"
        mask = out / f"{self.source_path.stem}_mask.png"
        self.result_rgba.save(cutout)
        self.processed_mask.save(mask)

        if self.raw_mask is not None:
            raw = out / f"{self.source_path.stem}_raw_mask.png"
            self.raw_mask.save(raw)

        self.status.set(f"Saved: {out}")
        messagebox.showinfo(APP_TITLE, self.tr("saved", path=out))

    def export_mask_for_edit(self):
        if self.processed_mask is None or not self.source_path:
            messagebox.showinfo(APP_TITLE, self.tr("need_mask"))
            return

        out = self.current_output_dir()
        path = out / f"{self.source_path.stem}_edit_mask.png"
        self.processed_mask.save(path)
        self.status.set(f"Edit mask exported: {path.name}")

        try:
            self._launch_mask_editor(path)
        except Exception as e:
            messagebox.showwarning(APP_TITLE, self.tr("editor_failed", error=e))

    def reload_edit_mask(self):
        if not self.source_path:
            messagebox.showinfo(APP_TITLE, self.tr("need_image"))
            return
        out = self.current_output_dir()
        path = out / f"{self.source_path.stem}_edit_mask.png"
        if not path.exists():
            messagebox.showinfo(APP_TITLE, self.tr("edit_mask_missing", path=path))
            return
        self.load_mask(path, source_kind="edited")

    def open_output_folder(self):
        out = self.current_output_dir() if self.source_path else self.output_root
        out.mkdir(parents=True, exist_ok=True)
        try:
            if os.name == "nt":
                os.startfile(str(out))
            else:
                subprocess.Popen(["xdg-open", str(out)])
        except Exception as e:
            messagebox.showerror(APP_TITLE, str(e))

    def reset_sliders(self):
        self.gamma_var.set(cfg_get(self.cfg, "defaults", "alpha_gamma", 0.72, float))
        self.offset_var.set(cfg_get(self.cfg, "defaults", "mask_offset", 0, int))
        self.blur_var.set(cfg_get(self.cfg, "defaults", "mask_blur", 0.0, float))
        self.black_var.set(cfg_get(self.cfg, "defaults", "black_threshold", 0, int))
        self.white_var.set(cfg_get(self.cfg, "defaults", "white_threshold", 250, int))
        self.reprocess_preview()

    def save_settings(self):
        if not self.cfg.has_section("defaults"):
            self.cfg.add_section("defaults")
        self.cfg["defaults"]["alpha_gamma"] = f"{self.gamma_var.get():.3f}"
        self.cfg["defaults"]["mask_offset"] = str(int(self.offset_var.get()))
        self.cfg["defaults"]["mask_blur"] = f"{self.blur_var.get():.2f}"
        self.cfg["defaults"]["black_threshold"] = str(int(self.black_var.get()))
        self.cfg["defaults"]["white_threshold"] = str(int(self.white_var.get()))
        if not self.cfg.has_section("ui"):
            self.cfg.add_section("ui")
        self.cfg["ui"]["language"] = self.language
        self.cfg["ui"]["sync_mask_preview"] = "1" if self.sync_mask_preview.get() else "0"
        if not self.cfg.has_section("paint"):
            self.cfg.add_section("paint")
        self.cfg["paint"]["mode"] = self.interaction_mode.get()
        self.cfg["paint"]["brush_color"] = self.brush_color.get()
        self.cfg["paint"]["brush_size"] = str(int(self.brush_size_var.get()))
        self._write_cfg()
        self.status.set(self.tr("settings_saved"))

    def _write_cfg(self):
        with self.cfg_path.open("w", encoding="utf-8") as f:
            self.cfg.write(f)

    def save_editor_mode(self):
        if not self.cfg.has_section("editor"):
            self.cfg.add_section("editor")
        self.cfg["editor"]["mode"] = self.editor_mode.get()
        self.cfg["editor"]["paintnet_aumid"] = self.paintnet_aumid
        self.cfg["editor"]["paintnet_desktop_path"] = self.paintnet_desktop_path
        self._write_cfg()
        self._refresh_editor_combo()
        self.status.set(f"Editor: {self._editor_mode_label()}")

    def _detect_paintnet_desktop(self) -> str | None:
        if os.name != "nt":
            return None

        candidates: list[Path] = []
        if self.paintnet_desktop_path:
            candidates.append(Path(self.paintnet_desktop_path))

        for executable in ("PaintDotNet.exe", "paintdotnet.exe"):
            found = shutil.which(executable)
            if found:
                candidates.append(Path(found))

        try:
            import winreg
            views = [0]
            if hasattr(winreg, "KEY_WOW64_64KEY"):
                views.extend([winreg.KEY_WOW64_64KEY, winreg.KEY_WOW64_32KEY])
            for hive in (winreg.HKEY_CURRENT_USER, winreg.HKEY_LOCAL_MACHINE):
                for view in views:
                    try:
                        with winreg.OpenKey(
                            hive,
                            r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\PaintDotNet.exe",
                            0,
                            winreg.KEY_READ | view,
                        ) as key:
                            value, _ = winreg.QueryValueEx(key, None)
                            if value:
                                candidates.append(Path(value.strip('"')))
                    except OSError:
                        pass
        except Exception:
            pass

        for base in (os.environ.get("ProgramFiles"), os.environ.get("ProgramFiles(x86)"), os.environ.get("LOCALAPPDATA")):
            if base:
                candidates.append(Path(base) / "paint.net" / "PaintDotNet.exe")

        seen = set()
        for candidate in candidates:
            try:
                resolved = str(candidate.expanduser().resolve())
            except Exception:
                resolved = str(candidate)
            key = resolved.lower()
            if key in seen:
                continue
            seen.add(key)
            if Path(resolved).is_file():
                self.paintnet_desktop_path = resolved
                return resolved
        return None

    def _has_store_paintnet(self) -> bool:
        if os.name != "nt":
            return False
        command = "if (Get-AppxPackage -Name 'dotPDNLLC.paint.net' -ErrorAction SilentlyContinue) { exit 0 } else { exit 1 }"
        try:
            result = subprocess.run(
                ["powershell.exe", "-NoLogo", "-NoProfile", "-NonInteractive", "-Command", command],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=8,
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
            )
            return result.returncode == 0
        except Exception:
            return False

    def _launch_store_paintnet(self, path: Path):
        target = f"shell:AppsFolder\\{self.paintnet_aumid}"
        subprocess.Popen(
            ["cmd.exe", "/d", "/c", "start", "", target, str(path)],
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )

    def _open_with_dialog(self, path: Path):
        if os.name == "nt":
            subprocess.Popen(["rundll32.exe", "shell32.dll,OpenAs_RunDLL", str(path)])
        else:
            subprocess.Popen(["xdg-open", str(path)])

    def _launch_mask_editor(self, path: Path):
        mode = self.editor_mode.get().strip()
        if mode == "windows_default":
            mode = "windows_open_with"
        editor = cfg_get(self.cfg, "editor", "mask_editor", "").strip().strip('"')

        if mode == "auto":
            desktop = self._detect_paintnet_desktop()
            if desktop:
                subprocess.Popen([desktop, str(path)])
                self.status.set(f"Editor: Paint.NET (Desktop) - {desktop}")
                return
            if self._has_store_paintnet():
                self._launch_store_paintnet(path)
                self.status.set("Editor: Paint.NET (Microsoft Store)")
                return
            self._open_with_dialog(path)
            self.status.set(self._editor_mode_label("windows_open_with"))
            return

        if mode == "paintnet_store":
            if self._has_store_paintnet():
                self._launch_store_paintnet(path)
                return
            messagebox.showinfo(APP_TITLE, self.tr("store_paintnet_missing"))
            self._open_with_dialog(path)
            return

        if mode == "paintnet_desktop":
            desktop = self._detect_paintnet_desktop()
            if desktop:
                subprocess.Popen([desktop, str(path)])
                return
            messagebox.showinfo(APP_TITLE, self.tr("desktop_paintnet_missing"))
            self._open_with_dialog(path)
            return

        if mode == "custom_exe":
            if editor and Path(editor).is_file():
                subprocess.Popen([editor, str(path)])
                return
            messagebox.showinfo(APP_TITLE, self.tr("custom_editor_missing", path=editor or "(not set)"))
            self._open_with_dialog(path)
            return

        self._open_with_dialog(path)

    def detect_paintnet(self):
        desktop = self._detect_paintnet_desktop()
        if desktop:
            self.editor_mode.set("paintnet_desktop")
            self.paintnet_desktop_path = desktop
            self.save_editor_mode()
            messagebox.showinfo(APP_TITLE, self.tr("paintnet_detected_desktop", path=desktop))
            return
        if self._has_store_paintnet():
            self.editor_mode.set("paintnet_store")
            self.save_editor_mode()
            messagebox.showinfo(APP_TITLE, self.tr("paintnet_detected_store"))
            return
        self.editor_mode.set("windows_open_with")
        self.save_editor_mode()
        messagebox.showinfo(APP_TITLE, self.tr("paintnet_not_found"))

    def choose_editor(self):
        path = filedialog.askopenfilename(
            title=self.tr("choose_editor"),
            filetypes=[("Executable", "*.exe"), ("All files", "*.*")],
        )
        if not path:
            return
        if not self.cfg.has_section("editor"):
            self.cfg.add_section("editor")
        self.cfg["editor"]["mask_editor"] = path
        self.cfg["editor"]["mode"] = "custom_exe"
        self.editor_mode.set("custom_exe")
        self._write_cfg()
        self._refresh_editor_combo()
        self.status.set(f"Editor: {path}")


def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--config", default=str(app_dir() / "config.ini"))
    parser.add_argument("image", nargs="?")
    args = parser.parse_args()

    cfg_path = Path(args.config)
    if not cfg_path.exists():
        messagebox.showerror(APP_TITLE, STRINGS["en"]["config_missing"].format(path=cfg_path))
        return

    app = App(cfg_path, initial_image=args.image)
    app.mainloop()


if __name__ == "__main__":
    main()
