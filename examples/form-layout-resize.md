# formLayout リサイズ対応 UI

ウィンドウリサイズに追従する配置。上部ボタン・下部ステータス・中央スクロール領域。

```python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import maya.cmds as cmds

WINDOW_NAME = "formLayoutToolWindow"


def deleteWindowIfExists():
    if cmds.window(WINDOW_NAME, exists=True):
        cmds.deleteUI(WINDOW_NAME, window=True)


def show():
    deleteWindowIfExists()
    cmds.window(WINDOW_NAME, title="Form Layout Tool", widthHeight=(400, 300), sizeable=True)

    rootForm = cmds.formLayout(numberOfDivisions=100)
    btnRun = cmds.button(label="Run")
    btnClose = cmds.button(label="Close", command=lambda *_: deleteWindowIfExists())

    scroll = cmds.scrollLayout(childResizable=True)
    cmds.columnLayout(adjustableColumn=True)
    for index in range(20):
        cmds.checkBox(label="Option {}".format(index + 1))
    cmds.setParent("..")
    cmds.setParent("..")

    status = cmds.text(label="Ready", align="left")

    cmds.formLayout(
        rootForm,
        edit=True,
        attachForm=[
            (btnRun, "top", 8),
            (btnRun, "left", 8),
            (btnClose, "top", 8),
            (btnClose, "right", 8),
            (scroll, "left", 8),
            (scroll, "right", 8),
            (status, "left", 8),
            (status, "right", 8),
            (status, "bottom", 8),
        ],
        attachControl=[
            (scroll, "top", 8, btnRun),
            (scroll, "bottom", 8, status),
        ],
        attachPosition=[
            (btnRun, "right", 8, 50),
            (btnClose, "left", 8, 50),
        ],
        attachNone=[
            (btnRun, "bottom"),
            (btnClose, "bottom"),
            (scroll, "bottom"),
            (status, "top"),
        ],
    )

    cmds.showWindow(WINDOW_NAME)


show()
```

## ポイント

- 各子について上下左右の attach を設計する  
- `attachPosition` で Run / Close を左右 50% 付近に分割  
- `scrollLayout` + `columnLayout` で項目数が多い UI に対応
