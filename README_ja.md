# InSpyCutout

**アニメ・イラスト向けの、ローカル動作するAI半自動背景切り抜き＋簡易マスク編集ツールです。**

[English README](README.md)

InSpyCutout は `transparent-background` 経由で **InSPyReNet** を使用し、まずAIにマスクを作らせます。その後、完全自動では残りがちな「あと少し」だけをスライダーや白黒ブラシでサッと直すことを目的にしています。

## 基本の流れ

1. 元画像を開く
2. InSpyReNet が自動でマスク生成
3. Alpha Gamma / Threshold / Blur / Mask Offset を透過プレビューを見ながら調整
4. 軽い修正なら白ブラシ（残す）・黒ブラシ（消す）で直接修正
5. 保存
6. 大きな修正が必要なら Paint.NET 等へマスクを書き出して、修正後に再読込

## 主な機能

- 初回セットアップ後はローカル処理
- InSpyReNet `base` を標準使用
- リアルタイム透過プレビュー
- 白黒ブラシによる簡易マスク修正
- ブラシサイズ変更、Undo / Redo
- マウスホイールでズーム
- 移動モードで左ドラッグしてパン
- ペイント中も **Space + 左ドラッグ** で一時移動
- **マウス中ボタンドラッグ** ならいつでも移動
- Black / White Threshold は 0～255
- 日本語 / English をワンクリック切替
- `output/元ファイル名/` 単位で自動整理
- Microsoft Store版 Paint.NET の起動に対応

## Windowsでの導入

1. Release ZIP をダウンロードして展開
2. **`Setup.bat`** をダブルクリック
3. 専用 `.venv` を作成し、必要ライブラリ・モデルを自動準備
4. デスクトップにショートカットを作成
5. ショートカットまたは `Launch_GUI.bat` から起動

Python 3.11 を使用します。Python 3.11 が無い場合、`winget` が利用できるWindowsではセットアップから導入できます。

NVIDIA GPUが見つかった場合はPyTorch公式のCUDA 12.8 wheel indexを使ってGPU版を導入し、それ以外は通常の依存関係を導入します。

## 操作

| 操作 | キー / マウス |
|---|---|
| 移動モード | `M` |
| ペイントモード | `B` |
| 白 / 黒ブラシ切替 | `X` |
| ブラシサイズ | `[` / `]` またはGUIスライダー |
| Undo | `Ctrl+Z` |
| Redo | `Ctrl+Y` / `Ctrl+Shift+Z` |
| ズーム | マウスホイール |
| 移動 | 移動モード + 左ドラッグ |
| ペイント中の一時移動 | `Space` を押しながら左ドラッグ |
| いつでも移動 | マウス中ボタンドラッグ |
| 全体表示 | ダブルクリック |

## マスクの意味

- **白** = 残す / 不透明
- **黒** = 消す / 透明
- **グレー** = 半透明

## 出力例

`sample.png` の場合：

```text
output/
  sample/
    sample_cutout.png
    sample_mask.png
    sample_raw_mask.png
    sample_edit_mask.png   # 外部編集へ書き出した場合
```

## 設定

`config.ini` にモデル、スライダー初期値、ブラシ、外部エディタ、言語などを保存します。

```ini
[ui]
language=auto
paint_preview_ms=90
```

`language=auto` の場合、日本語環境では日本語、それ以外では英語で起動します。GUI右上のボタンからワンクリックで切り替えでき、その選択は保存されます。

## このツールの狙い

AI切り抜きはすでにかなり高精度ですが、髪の毛一本、背景の残骸、小さな穴などで「あと少し」修正したくなるケースがあります。InSpyCutout は本格的な画像編集ソフトを目指すのではなく、その最後の数％を短時間で直すことに重点を置いています。

## クレジット

背景除去には [transparent-background](https://github.com/plemeri/transparent-background) と [InSPyReNet](https://github.com/plemeri/InSPyReNet) を利用しています。

## ライセンス

InSpyCutout 本体は [MIT License](LICENSE) です。依存関係については [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) を参照してください。
