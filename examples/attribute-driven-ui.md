# 属性連動 UI

選択ノードの属性を `attrFieldSliderGrp` で表示。選択変更時に UI を更新。

```python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import maya.cmds as cmds

WINDOW_NAME = "attrDrivenToolWindow"
ATTR_SLIDER = None
STATUS_TEXT = None


def deleteWindowIfExists():
    if cmds.window(WINDOW_NAME, exists=True):
        cmds.deleteUI(WINDOW_NAME, window=True)


def getTargetNode():
    selectionList = cmds.ls(selection=True, type="transform") or []
    if not selectionList:
        return None
    return selectionList[0]


def refreshUi(*_):
    global ATTR_SLIDER, STATUS_TEXT
    targetNode = getTargetNode()
    if targetNode is None:
        cmds.text(STATUS_TEXT, edit=True, label="Select a transform.")
        cmds.attrFieldSliderGrp(ATTR_SLIDER, edit=True, enable=False)
        return

    attrPath = "{}.translateX".format(targetNode)
    if not cmds.objExists(attrPath):
        cmds.text(STATUS_TEXT, edit=True, label="Missing translateX.")
        return

    cmds.attrFieldSliderGrp(
        ATTR_SLIDER,
        edit=True,
        attribute=attrPath,
        label="Translate X",
        enable=True,
    )
    cmds.text(STATUS_TEXT, edit=True, label="Node: {}".format(targetNode))


def show():
    global ATTR_SLIDER, STATUS_TEXT
    deleteWindowIfExists()
    cmds.window(WINDOW_NAME, title="Attribute UI", widthHeight=(300, 100))

    cmds.columnLayout(adjustableColumn=True, rowSpacing=8)
    STATUS_TEXT = cmds.text(label="Select a transform.", align="left")
    ATTR_SLIDER = cmds.attrFieldSliderGrp(
        label="Translate X",
        attribute="pCube1.translateX",
        enable=False,
    )
    cmds.button(label="Refresh from Selection", command=refreshUi)
    cmds.showWindow(WINDOW_NAME)
    refreshUi()


show()
```

## ポイント

- `attrFieldSliderGrp` に `attribute="node.attr"` を渡すとスライダと属性が連動  
- 存在しない属性パスは `cmds.objExists` で確認してから接続  
- 複数属性は `attrFieldGrp` / `attrControlGrp` も検討
