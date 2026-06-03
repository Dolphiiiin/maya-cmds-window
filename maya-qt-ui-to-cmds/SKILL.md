---
name: maya-qt-ui-to-cmds
description: >
  Converts Qt Designer .ui files and PySide uic output into hand-written maya.cmds
  window/layout/control Python only. Does not output loadUI, PySide, PyQt, or Qt
  runtime code. Use when migrating .ui or PySide tools to pure cmds UI scripts.
---

# PySide / Qt UI → maya.cmds 変換

## 基本方針（必須）

| 項目 | 方針 |
|------|------|
| **入力** | `.ui` XML、`Ui_*`（pyside-uic）、既存 PySide コード（**設計図として読むだけ**） |
| **出力** | `maya.cmds` による UI 構築 Python のみ |
| **禁止（出力に含めない）** | `cmds.loadUI` / `uiFile` / `uiString` |
| **禁止（出力に含めない）** | `PySide` / `PySide2` / `PySide6` / `PyQt` / `shiboken` |
| **禁止（出力に含めない）** | `QUiLoader` / `QtWidgets` / `QtCore` / `sip` / `wrapInstance` |
| **禁止（出力に含めない）** | 実行時の `.ui` 読み込み・Qt ウィンドウの `show()` |

`.ui` は **実行時に読み込まない**。構造と `objectName`・プロパティを解析し、**cmds で同等 UI を再実装したソースコード**を生成する。

変換後の実装規約は親スキル [maya-cmds-window](../SKILL.md) に従う。  
共通規約（**VERSION 付きタイトル**・**シーン切替時の開き直し**）: [tool-conventions.md](../reference/tool-conventions.md)

## 成果物の形

```python
import maya.cmds as cmds


class MyToolWindow(object):
    WINDOW_NAME = "myToolWindow"
    VERSION = "1.0.0"
    WINDOW_TITLE = "{} v{}".format(WINDOW_NAME, VERSION)

    def __init__(self):
        self.reopenOnSceneChange = True  # シーン横断ツールのみ False
        self.sceneScriptJobIdList = []
        self.runButton = None

    def buildUi(self):
        cmds.window(self.WINDOW_NAME, title=self.WINDOW_TITLE, widthHeight=(300, 200))
        cmds.columnLayout(adjustableColumn=True)
        self.runButton = cmds.button(label="Run", command=self.onRun)

    def show(self):
        self.deleteWindowIfExists()
        self.buildUi()
        self.installSceneReopenCallbacks()
        cmds.showWindow(self.WINDOW_NAME)
```

- `import maya.cmds as cmds`（およびプロジェクトで許容される `maya.mel` の最小利用）のみ  
- UI 定義は **関数内の cmds 呼び出しの並び**  
- コールバックは **Python 関数**を `command` / `closeCommand` に渡す  

## 標準ワークフロー

1. `.ui` または `setupUi` から階層・`objectName`・主要 `property` を抽出  
2. `scripts/parse_ui_outline.py` でアウトラインを確認（任意）  
3. [reference/widget-mapping.md](reference/widget-mapping.md) で Qt → cmds を対応付け  
4. ルート `QDialog` / `QWidget` → `cmds.window` + ルート layout  
5. 子を深さ優先で `columnLayout` / `formLayout` / `button` 等に変換  
6. `connections` / PySide `connect` → `command` 関数へ置換  
7. 単一インスタンス（`exists` + `deleteUI`）、`showWindow`  
8. 未対応 Qt 部品は cmds で代替設計し、コメントで差分を明示  

詳細: [reference/conversion-workflow.md](reference/conversion-workflow.md)

### 出力前チェックリスト

- [ ] 出力コードに `loadUI` が無いか  
- [ ] `PySide` / `Qt` / `QUiLoader` の import が無いか  
- [ ] `.ui` パスを実行時に開いていないか  
- [ ] UI クラスにまとまり、`self` でパラメータを保持しているか  
- [ ] `WINDOW_TITLE = "{} v{}".format(WINDOW_NAME, VERSION)` か  
- [ ] シーン依存 UI なら `self.reopenOnSceneChange` と scriptJob があるか  
- [ ] ウィンドウ直下が layout か  
- [ ] 全コールバックが cmds の `command` 等か  
- [ ] `QDialogButtonBox` を個別 `button` に分解したか  

## 入力の読み方

| 入力 | 読み方 |
|------|--------|
| `.ui` | XML。 [reference/ui-file-anatomy.md](reference/ui-file-anatomy.md) |
| `Ui_*` / `setupUi` | 階層の参考。 [reference/pyside-uic-to-cmds.md](reference/pyside-uic-to-cmds.md) |
| 既存 PySide ツール | ウィジェット樹とシグナル接続を抽出し、cmds へ写す |

`pyside-uic` 生成物は **入力解析用**。出力に `Ui_*` 継承や `setupUi(self)` を残さない。

## cmds で再現できないもの

| Qt | 対応 |
|----|------|
| `styleSheet` | 再現不可。必要なら `backgroundColor` 等の限定フラグのみ |
| `QDialogButtonBox` | `rowLayout` + 複数 `button` |
| 複雑な `QListWidget` セル UI | `textScrollList` 等へ簡略化 |
| `QWebEngineView` 等 | 機能削減または別手段をコメントで提案 |

再現不可の場合は **cmds で可能な代替**を実装し、差分をコメントで残す。

## 解析ツール

```bash
python maya-qt-ui-to-cmds/scripts/parse_ui_outline.py path/to/dialog.ui
```

## やらないこと

- 出力に `cmds.loadUI(uiFile=...)` を書く  
- 出力に PySide で `.ui` を読み込むコードを残す  
- 「とりあえず loadUI で動く」ことを変換完了とする  
- cmds に無い API をあるかのように書く  

## 参考（出力には使わない）

Maya の `loadUI` が Qt クラスをどの cmds に対応付けるかは、マッピング調査の参考にできる。エージェントは **出力コードに loadUI を書かない**。  
[reference/loadui-mapping-reference.md](reference/loadui-mapping-reference.md)

## 追加リソース

| ファイル | 内容 |
|----------|------|
| [reference/conversion-workflow.md](reference/conversion-workflow.md) | 変換手順の詳細 |
| [reference/widget-mapping.md](reference/widget-mapping.md) | Qt → cmds 対応表 |
| [reference/ui-file-anatomy.md](reference/ui-file-anatomy.md) | .ui XML |
| [reference/pyside-uic-to-cmds.md](reference/pyside-uic-to-cmds.md) | Ui_* 入力の読み方 |
| [examples/manual-rewrite-dialog.md](examples/manual-rewrite-dialog.md) | 出力サンプル |
| [examples/from-uic-class.md](examples/from-uic-class.md) | Ui_* 入力 → cmds 出力 |

## 公式（入力側の理解用）

- [cat_Windows / cmds UI](https://help.autodesk.com/cloudhelp/JPN/MayaCRE-Tech-Docs/CommandsPython/cat_Windows.html)
- [cmds ウィンドウ構築スキル](../SKILL.md)
