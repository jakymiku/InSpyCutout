# InSpyCutout

**アニメ・イラスト・AI画像・写真に使える、ローカル動作のAI半自動背景切り抜き＋簡易マスク編集ツールです。**

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
- モデルやパッケージのアプリ専用キャッシュもInSpyCutoutフォルダ内に保存
- InSpyReNet `base` を標準使用
- アニメ・イラスト系だけでなく、写真風AI画像や一般的な写真にも利用可能
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
- Paint.NET（Microsoft Store版 / デスクトップ版）の自動検出と、Windows「プログラムから開く…」に対応
- カメラ・スマホ画像のEXIF回転を自動反映
- 元画像に既存の透過がある場合、その透明部分をAI/手動マスクで誤って不透明に戻さない
- 外部編集マスクのサイズが元画像と違う場合は自動リサイズせず、安全のため読み込みを中止

## Windowsでの導入

1. Release ZIP をダウンロードして展開
2. **`Setup.bat`** をダブルクリック
3. 専用 `.venv` を作成し、必要ライブラリ・モデルを自動準備
4. デスクトップにショートカットを作成
5. ショートカットまたは `Launch_GUI.bat` から起動

Python 3.11 を使用します。Python 3.11 が無い場合、`winget` が利用できるWindowsではセットアップから導入できます。

専用Python環境は `.venv/`、InSPyReNetモデル・pipキャッシュ・PyTorch関連キャッシュなどのアプリ専用キャッシュは `cache/` に保存します。ComfyUIなど、他のPython環境へパッケージをインストールしません。

NVIDIA GPUが見つかった場合はPyTorch公式のCUDA 12.8 wheel indexを使ってGPU版を導入し、それ以外は通常の依存関係を導入します。

Windowsでの再現性を優先し、`transparent-background 1.3.4`、`albumentations 1.4.16`、`albucore 0.0.17` を固定しています。これにより、新しいAlbucore/StringZilla系依存関係が環境によってC/C++のローカルビルドへフォールバックする問題を避けます。

`Setup.bat` 実行時にはアプリフォルダ直下へ **`setup.log`** も保存します。セットアップが失敗した場合や、コンソールの表示が流れて消えてしまった場合は、このファイルをそのまま添付してください。

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

### 外部マスクエディター

標準は **`自動検出 (推奨)`** です。マスクを書き出して編集するとき、InSpyCutout は次の順でエディターを探します。

1. デスクトップ版 Paint.NET（レジストリ、PATH、標準的なインストール先を確認）
2. Microsoft Store版 Paint.NET
3. 見つからなければ Windows の **「プログラムから開く…」** を表示

Store版 Paint.NET は固定インストールパスを直接参照せず、WindowsのアプリID経由で起動するため、同じMicrosoft Store版をインストールしている他のPCでも利用できます。デスクトップ版Paint.NETも自動検出します。

Paint.NET以外を常用する場合は **「カスタムEXEを選択」** から Krita / GIMP / その他の画像編集ソフトの実行ファイルを指定できます。旧 `Windows default` 相当の「PNGの既定アプリをそのまま開く」動作は、画像ビューアーが起動することが多いため標準候補から外し、代わりに「プログラムから開く…」を使用します。

## 削除・アンインストール

InSpyCutoutを終了し、必要なら `output/` の画像を退避してから、展開した **InSpyCutoutフォルダを丸ごと削除**してください。アプリ本体、専用 `.venv`、ダウンロードしたモデル、アプリ専用キャッシュ、設定、出力ファイルはこのフォルダ内に保存されます。

フォルダ外に残る可能性があるものは次の2つです。

- **Python 3.11**：SetupがPython 3.11を新規インストールした場合、他のアプリが利用している可能性があるため自動削除しません。Python 3.11を他で利用していなければ、後ほど **Windowsの設定 > アプリ > インストールされているアプリ** から手動でアンインストールしてください。
- **デスクトップショートカット**：アプリフォルダを削除してもショートカットは自動では消えません。残っていた場合は手動で削除してください。デフォルト名は **`InSpyCutout`**（`InSpyCutout.lnk`）です。名前を変更していた場合は、変更後のショートカットを削除してください。

この構成のため、専用のアンインストールBATは用意していません。

## このツールの狙い

AI切り抜きはすでにかなり高精度ですが、髪の毛一本、背景の残骸、小さな穴などで「あと少し」修正したくなるケースがあります。InSpyCutout は本格的な画像編集ソフトを目指すのではなく、その最後の数％を短時間で直すことに重点を置いています。

## クレジット

背景除去には [transparent-background](https://github.com/plemeri/transparent-background) と [InSPyReNet](https://github.com/plemeri/InSPyReNet) を利用しています。

## ライセンス

InSpyCutout 本体は [MIT License](LICENSE) です。依存関係については [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) を参照してください。
