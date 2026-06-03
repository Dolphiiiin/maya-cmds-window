---
name: maya-cmds-window
description: >
  Builds Maya tool UIs using maya.cmds window, layout, control, menu, and panel
  commands only (no PySide, PyMEL, or Qt). Use when creating cmds.window,
  formLayout, columnLayout, showWindow, dockControl, modelPanel embedding,
  attrFieldGrp, confirmDialog, or any UI from Autodesk cat_Windows documentation.
---

# Maya cmds ウィンドウ構築

## スコープ境界

| 使用する | 使用しない |
|----------|------------|
| `maya.cmds` の UI コマンド | PySide / PySide2 / PySide6 |
| 最小限の `maya.mel.eval`（例: `$gMainWindow`） | PyMEL |
| `confirmDialog` 等の cmds ダイアログ | Qt 直接操作 |
| `modelPanel` 等のパネル埋め込み | OpenMayaUI でのウィンドウ構築 |

ユーザーのプロジェクト Python 規約がある場合は **スタイルをそちらに合わせ**、本スキルは **API と UI 構築手順**に集中する。

## ツール共通規約

詳細: [reference/tool-conventions.md](reference/tool-conventions.md)

### UI クラス

- ウィンドウ構築・コールバック・状態は **1 つの UI クラス**にまとめる  
- `WINDOW_NAME` / `VERSION` / control 名・ツールパラメータは **`self` またはクラス定数**で保持  
- モジュールの `show()` はインスタンスを生成して `ui.show()` を呼ぶ  

### バージョン表記

- クラス定数 `WINDOW_NAME`, `VERSION` を定義する  
- 定数連結: `WINDOW_TITLE = "{} v{}".format(WINDOW_NAME, VERSION)`（例: `basicToolWindow v1.0.0`）  
- `cmds.window(..., title=self.WINDOW_TITLE)`  

### シーン切り替え時の開き直し

- **推奨（既定）**: `self.reopenOnSceneChange = True`。`NewSceneOpened` / `SceneOpened` で `deleteUI` 後に再 `show`  
- **例外**: シーン横断ツールは `self.reopenOnSceneChange = False`（理由をコメントで残す）  
- `self.sceneScriptJobIdList` で scriptJob を管理し、閉鎖時に `kill`  

## 標準ワークフロー

1. ウィンドウ名で `cmds.window(name, exists=True)` を照会  
2. 既存なら `cmds.deleteUI(name, window=True)`  
3. `cmds.window(name, ...)` で作成（この時点では **非表示**）  
4. 必要なら `uiTemplate` を設定（`window` は uiTemplate スタックを **クリア**する）  
5. **layout** を作成（ウィンドウ直下に control は置けない）  
6. control を追加、`setParent('..')` で階層を戻す  
7. `command` / `closeCommand` に **Python 関数**を渡す  
8. `cmds.showWindow(name)` で表示  

### チェックリスト

- [ ] 子 UI 構築後に `showWindow` したか  
- [ ] ウィンドウ直下が layout か  
- [ ] 単一インスタンスなら `exists` + `deleteUI` か  
- [ ] UI クラスにまとまり、パラメータが `self` で保持されているか  
- [ ] `WINDOW_TITLE = "{} v{}".format(WINDOW_NAME, VERSION)` か  
- [ ] シーン依存ツールでシーン切替時の開き直しがあるか（横断ツールは `reopenOnSceneChange = False`）  
- [ ] formLayout で各方向に attach があるか（循環 attach なし）  
- [ ] 文字列コールバックで `deleteUI` のエスケープ事故がないか  

## レイアウト選定

| 用途 | 推奨 |
|------|------|
| 縦並びツール | `columnLayout`（`adjustableColumn=True`） |
| リサイズ追従 | `formLayout`（`attachForm` / `attachControl` / `attachPosition`） |
| 横並び | `rowLayout` / `flowLayout` |
| グリッド | `gridLayout` |
| 長い UI | `scrollLayout` で包む |
| タブ | `tabLayout` |
| 折りたたみグループ | `frameLayout`（`collapsable=True`） |
| ビューポート埋め込み | `paneLayout` + `modelPanel` 等 |

### formLayout の注意

- 各子について、上下左右の **少なくとも各方向 1 エッジ**を attach する  
- 子同士の attach が **循環**すると Maya が警告し無視する  
- `numberOfDivisions`（既定 100）を基準に `attachPosition` の比率を指定  

## コールバック

- `command` / `closeCommand` には **関数オブジェクト**を渡す（推奨）  
- 文字列コールバックはウィンドウ名のクォート事故が起きやすい  
- UI 名を渡す場合はモジュールレベル関数 + 固定ウィンドウ名、または `functools.partial`  

## やらないこと

- PySide / QWidget の提案 → cmds で代替を提示  
- PyMEL の UI ラッパー → cmds に書き直す  
- `cmds.error` 等の強いエラー表示（プロジェクト規約に従う）  

## 追加リソース

| ファイル | 内容 |
|----------|------|
| [reference/commands-index.md](reference/commands-index.md) | cat_Windows 全コマンド索引 |
| [reference/tool-conventions.md](reference/tool-conventions.md) | VERSION・シーン切替時の開き直し |
| [reference/window-lifecycle.md](reference/window-lifecycle.md) | window / showWindow / deleteUI 等 |
| [reference/layouts.md](reference/layouts.md) | レイアウトコマンド詳細 |
| [reference/controls.md](reference/controls.md) | コントロール群 |
| [reference/menus.md](reference/menus.md) | メニュー |
| [reference/panels.md](reference/panels.md) | パネル・エディタ |
| [reference/dialogs-and-misc.md](reference/dialogs-and-misc.md) | ダイアログ・その他 UI |
| [examples/](examples/) | 実装パターンサンプル |

## 実装パターンへのリンク

| パターン | 例 |
|----------|-----|
| 基本ツールウィンドウ | [examples/basic-tool-window.md](examples/basic-tool-window.md) |
| リサイズ対応 formLayout | [examples/form-layout-resize.md](examples/form-layout-resize.md) |
| タブ・スクロール・リスト | [examples/tabs-scroll-lists.md](examples/tabs-scroll-lists.md) |
| 属性 UI | [examples/attribute-driven-ui.md](examples/attribute-driven-ui.md) |
| メニュー・ポップアップ | [examples/menus-popup.md](examples/menus-popup.md) |
| パネル埋め込み | [examples/panel-in-window.md](examples/panel-in-window.md) |

## 関連スキル

PySide / Qt Designer の `.ui` を cmds 手書きコードへ変換する場合は [maya-qt-ui-to-cmds](maya-qt-ui-to-cmds/SKILL.md) を使用する（出力に PySide・loadUI は含めない）。

## 公式ドキュメント

ベース URL: `https://help.autodesk.com/cloudhelp/JPN/MayaCRE-Tech-Docs/CommandsPython/`

カテゴリ索引: [cat_Windows.html](https://help.autodesk.com/cloudhelp/JPN/MayaCRE-Tech-Docs/CommandsPython/cat_Windows.html)
