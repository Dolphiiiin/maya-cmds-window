# 例: .ui から cmds 手書き出力

`.ui` を入力とし、UI クラス + `WINDOW_NAME vVERSION` 形式で cmds のみ再構築した例。

## 想定 .ui 構造

```
QDialog "MyToolDialog"
  QVBoxLayout "mainLayout"
    QLabel "titleLabel"
    QHBoxLayout "buttonRow"
      QPushButton "executeBtn"
      QPushButton "closeBtn"
```

## 変換後 cmds

```python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import maya.cmds as cmds


class MyToolDialogWindow(object):
    """MyToolDialog .ui から変換した cmds UI"""

    WINDOW_NAME = "MyToolDialog"
    VERSION = "1.0.0"
    WINDOW_TITLE = "{} v{}".format(WINDOW_NAME, VERSION)

    def __init__(self):
        self.reopenOnSceneChange = True
        self.sceneScriptJobIdList = []
        self.titleLabel = None
        self.executeBtn = None
        self.closeBtn = None

    def deleteWindowIfExists(self):
        if cmds.window(self.WINDOW_NAME, exists=True):
            cmds.deleteUI(self.WINDOW_NAME, window=True)

    def removeSceneReopenCallbacks(self):
        for jobId in self.sceneScriptJobIdList:
            if cmds.scriptJob(exists=jobId):
                cmds.scriptJob(kill=jobId, force=True)
        self.sceneScriptJobIdList = []

    def installSceneReopenCallbacks(self):
        self.removeSceneReopenCallbacks()
        if not self.reopenOnSceneChange:
            return
        for eventName in ["NewSceneOpened", "SceneOpened"]:
            jobId = cmds.scriptJob(e=True, event=[eventName, self.onSceneChanged])
            self.sceneScriptJobIdList.append(jobId)

    def onSceneChanged(self, *_):
        self.show()

    def onExecute(self, *_):
        cmds.inViewMessage(amg="<hl>Execute</hl>", pos="midCenter", fade=True)

    def onClose(self, *_):
        self.removeSceneReopenCallbacks()
        self.deleteWindowIfExists()

    def buildUi(self):
        cmds.window(
            self.WINDOW_NAME,
            title=self.WINDOW_TITLE,
            widthHeight=(280, 100),
            sizeable=True,
            closeCommand=self.onClose,
        )
        cmds.columnLayout(adjustableColumn=True, rowSpacing=8)
        self.titleLabel = cmds.text(
            "titleLabel",
            label="Run tool on selection",
            align="center",
        )
        cmds.rowLayout(
            "buttonRow",
            numberOfColumns=2,
            columnWidth2=(130, 130),
            columnAttach2=("both", "both"),
        )
        self.executeBtn = cmds.button("executeBtn", label="Execute", command=self.onExecute)
        self.closeBtn = cmds.button("closeBtn", label="Close", command=self.onClose)
        cmds.setParent("..")

    def show(self):
        self.deleteWindowIfExists()
        self.buildUi()
        self.installSceneReopenCallbacks()
        cmds.showWindow(self.WINDOW_NAME)


_myToolDialogWindow = None


def show():
    global _myToolDialogWindow
    if _myToolDialogWindow is None:
        _myToolDialogWindow = MyToolDialogWindow()
    _myToolDialogWindow.show()


show()
```

## マッピングメモ

| Qt | cmds |
|----|------|
| `objectName` / `QDialog` | クラス定数 `WINDOW_NAME` + `WINDOW_TITLE` |
| `windowTitle` | `WINDOW_TITLE`（`WINDOW_NAME vVERSION`） |
| `QVBoxLayout` | `columnLayout` |
| `QHBoxLayout` | `rowLayout` + `setParent('..')` |
| control | `self` に UI 名を保持 |

`QDialogButtonBox` は使わず、ボタンを個別配置している。
