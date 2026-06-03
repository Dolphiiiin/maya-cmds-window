# 基本ツールウィンドウ

UI クラス + `WINDOW_NAME vVERSION` タイトル + シーン切替時の開き直し。

```python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import maya.cmds as cmds


class BasicToolWindow(object):
    """基本ツール UI"""

    WINDOW_NAME = "basicToolWindow"
    VERSION = "1.0.0"
    WINDOW_TITLE = "{} v{}".format(WINDOW_NAME, VERSION)

    def __init__(self):
        self.reopenOnSceneChange = True
        self.sceneScriptJobIdList = []
        self.runButton = None

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
        self.deleteWindowIfExists()
        self.show()

    def onRun(self, *_):
        selectionList = cmds.ls(selection=True) or []
        if not selectionList:
            cmds.inViewMessage(amg="<hl>Nothing selected</hl>", pos="midCenter", fade=True)
            return
        cmds.inViewMessage(
            amg="<hl>{}</hl>".format(len(selectionList)),
            pos="midCenter",
            fade=True,
        )

    def onClose(self, *_):
        self.removeSceneReopenCallbacks()
        self.deleteWindowIfExists()

    def buildUi(self):
        cmds.window(
            self.WINDOW_NAME,
            title=self.WINDOW_TITLE,
            widthHeight=(240, 120),
            sizeable=True,
            closeCommand=self.onClose,
        )
        cmds.columnLayout(adjustableColumn=True, rowSpacing=8)
        cmds.text(label="Select nodes and run.", align="center")
        self.runButton = cmds.button(label="Run", height=32, command=self.onRun)
        cmds.button(label="Close", command=self.onClose)

    def show(self):
        self.deleteWindowIfExists()
        self.buildUi()
        self.installSceneReopenCallbacks()
        cmds.showWindow(self.WINDOW_NAME)


_toolWindow = None


def show():
    global _toolWindow
    if _toolWindow is None:
        _toolWindow = BasicToolWindow()
    _toolWindow.show()


show()
```

## ポイント

- `WINDOW_TITLE` は `WINDOW_NAME` と `VERSION` の定数連結  
- UI 状態は `self`（`runButton`, `sceneScriptJobIdList` 等）  
- シーン横断ツールは `self.reopenOnSceneChange = False`（[tool-conventions.md](../reference/tool-conventions.md)）  
