# maya-cmds-window

Autodesk Maya の `maya.cmds` ウィンドウ API 向け Agent Skill 集です。

| スキル | 用途 |
|--------|------|
| [maya-cmds-window](SKILL.md) | cmds のみでウィンドウ / UI を構築 |
| [maya-qt-ui-to-cmds](maya-qt-ui-to-cmds/SKILL.md) | `.ui` / PySide UI を **cmds 手書きコード**へ変換（出力に PySide・loadUI なし） |

## maya-cmds-window

[cat_Windows](https://help.autodesk.com/cloudhelp/JPN/MayaCRE-Tech-Docs/CommandsPython/cat_Windows.html) に掲載される UI コマンドを対象とし、**PySide / PyMEL は使用しません**。

| パス | 内容 |
|------|------|
| `SKILL.md` | エージェント向けエントリ（ワークフロー・VERSION・シーン切替時の開き直し） |
| `reference/tool-conventions.md` | UI クラス・`WINDOW_NAME vVERSION`・scriptJob 規約 |
| `reference/` | コマンド索引とカテゴリ別リファレンス |
| `examples/` | よくある UI パターンの cmds サンプル |
| `scripts/fetch_docs.py` | 公式 HTML から索引を再生成するメンテ用スクリプト |

## maya-qt-ui-to-cmds

Qt Designer の `.ui` や `pyside-uic` 出力を **入力**とし、実行時に PySide / Qt / `loadUI` を使わない **cmds UI 構築 Python** を生成するスキルです。

| パス | 内容 |
|------|------|
| `maya-qt-ui-to-cmds/SKILL.md` | 基本方針・出力禁止事項・ワークフロー |
| `maya-qt-ui-to-cmds/reference/` | ウィジェット対応表・変換手順 |
| `maya-qt-ui-to-cmds/examples/` | cmds のみの出力サンプル |
| `maya-qt-ui-to-cmds/scripts/parse_ui_outline.py` | `.ui` 解析アウトライン生成 |

```bash
python maya-qt-ui-to-cmds/scripts/parse_ui_outline.py path/to/dialog.ui
```

## インストール（Cursor）

各スキルを個別にリンクします。

```bash
git clone <repository-url> maya-cmds-window
ln -s "$(pwd)/maya-cmds-window" ~/.cursor/skills/maya-cmds-window
ln -s "$(pwd)/maya-cmds-window/maya-qt-ui-to-cmds" ~/.cursor/skills/maya-qt-ui-to-cmds
```

Windows の場合は、管理者権限のある場所へコピーするか、junction を利用してください。

## 使い方

1. Cursor のエージェントチャットで `@maya-cmds-window` を指定する  
2. または、Maya の cmds でウィンドウ / UI を作る依頼をする（description による自動選択）

エージェントはまず `SKILL.md` を読み、必要に応じて `reference/` と `examples/` を参照します。

## ドキュメントの更新

公式ページの構成が変わった場合:

```bash
cd maya-cmds-window
python scripts/fetch_docs.py
```

`reference/commands-index.md` が再生成されます。高頻度コマンドの詳細は `reference/*.md` を手動で追記してください。

## スコープ

- **対象**: `maya.cmds` のウィンドウ・レイアウト・コントロール・メニュー・パネル・関連 UI  
- **対象外**: PySide、PyMEL、Qt 直接操作、`maya.api.OpenMayaUI` によるウィンドウ構築

プロジェクト固有の Python コーディング規約がある場合は、そちらをコードスタイルとして優先してください。本スキルは API 選択と UI 構築手順に集中します。

## ライセンス

Apache License 2.0
