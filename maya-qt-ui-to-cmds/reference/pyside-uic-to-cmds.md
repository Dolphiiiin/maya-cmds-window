# pyside-uic 出力の読み方（入力専用）

`pyside-uic` が生成した `Ui_<ClassName>` は **変換の入力**として使う。  
**出力コードに PySide / `setupUi` / `QtWidgets` を残さない。**

## 入力の種類

| 入力 | 使い方 |
|------|--------|
| `design.ui` | 正とする解析元 |
| `ui_design.py` | `setupUi` の階層・objectName の参考 |

開発者が手元で uic を実行するのは任意。配布するツールには **cmds のみ**を含める。

## setupUi から読み取る情報

```python
# 入力例（出力に含めない）
class Ui_Dialog(object):
    def setupUi(self, Dialog):
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.runButton = QtWidgets.QPushButton(Dialog)
        self.runButton.setObjectName("runButton")
```

| setupUi の記述 | cmds 出力 |
|----------------|-----------|
| `QVBoxLayout(Dialog)` | `cmds.columnLayout(...)` |
| `QPushButton` + `setObjectName` | `cmds.button("runButton", ...)` |
| `addWidget` の順序 | control の作成順（上→下） |
| `setText` / `retranslateUi` | `label` / `title` 初期値 |
| `.connect` / `connectSlotsByName` | `command=` へ関数を割当 |

## 出力の形（必須）

```python
import maya.cmds as cmds


class DialogWindow(object):
    WINDOW_NAME = "Dialog"
    VERSION = "1.0.0"
    WINDOW_TITLE = "{} v{}".format(WINDOW_NAME, VERSION)

    def __init__(self):
        self.runButton = None

    def buildUi(self):
        cmds.window(self.WINDOW_NAME, title=self.WINDOW_TITLE, ...)
        cmds.columnLayout(adjustableColumn=True)
        self.runButton = cmds.button("runButton", label="Run", command=self.onRun)
```

## やってはいけない出力

```python
# NG
from PySide2 import QtWidgets
class Tool(QtWidgets.QDialog, Ui_Tool):
    def __init__(self):
        self.setupUi(self)
```

```python
# NG
import ui_design
ui_design.Ui_Dialog().setupUi(self)
```

## 手順

1. `.ui` を優先して解析（[ui-file-anatomy.md](ui-file-anatomy.md)）  
2. `setupUi` で矛盾がないか確認  
3. [widget-mapping.md](widget-mapping.md) で cmds コマンドを決定  
4. [conversion-workflow.md](conversion-workflow.md) に従い Python を生成  

## 関連例

[from-uic-class.md](../examples/from-uic-class.md)
