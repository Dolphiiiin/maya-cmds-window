# 例: Ui_* クラスから cmds へ（出力サンプル）

`pyside-uic` の `setupUi` を **入力として読み**、UI クラス + cmds のみで出力する。

## 元の setupUi（抜粋・入力）

```python
class Ui_MyTool(object):
    def setupUi(self, MyTool):
        self.verticalLayout = QtWidgets.QVBoxLayout(MyTool)
        self.checkVerbose = QtWidgets.QCheckBox(MyTool)
        self.runBtn = QtWidgets.QPushButton(MyTool)
```

## cmds 変換（出力）

```python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import maya.cmds as cmds


class MyToolWindow(object):
    """Ui_MyTool から変換"""

    WINDOW_NAME = "MyTool"
    VERSION = "1.0.0"
    WINDOW_TITLE = "{} v{}".format(WINDOW_NAME, VERSION)

    def __init__(self):
        self.reopenOnSceneChange = True
        self.sceneScriptJobIdList = []
        self.checkVerbose = None
        self.runBtn = None

    def deleteWindowIfExists(self):
        if cmds.window(self.WINDOW_NAME, exists=True):
            cmds.deleteUI(self.WINDOW_NAME, window=True)

    def isVerbose(self):
        return cmds.checkBox(self.checkVerbose, query=True, value=True)

    def onRun(self, *_):
        verbose = self.isVerbose()
        message = "Run verbose" if verbose else "Run"
        cmds.inViewMessage(amg="<hl>{}</hl>".format(message), pos="midCenter", fade=True)

    def buildUi(self):
        cmds.window(self.WINDOW_NAME, title=self.WINDOW_TITLE, widthHeight=(300, 120))
        cmds.columnLayout(adjustableColumn=True, rowSpacing=6)
        self.checkVerbose = cmds.checkBox("checkVerbose", label="Verbose", value=False)
        self.runBtn = cmds.button("runBtn", label="Run", command=self.onRun)

    def show(self):
        self.deleteWindowIfExists()
        self.buildUi()
        cmds.showWindow(self.WINDOW_NAME)


_myToolWindow = None


def show():
    global _myToolWindow
    if _myToolWindow is None:
        _myToolWindow = MyToolWindow()
    _myToolWindow.show()
```

## 手順の対応

| setupUi | cmds 出力 |
|---------|-----------|
| ルート objectName | `WINDOW_NAME` / `WINDOW_TITLE` |
| `QVBoxLayout` | `columnLayout` |
| widget 変数 | `self.checkVerbose` 等 |
| `connect` / スロット | `command=self.onRun` |

出力に `PySide` / `setupUi` / `Ui_*` 継承は含めない。
