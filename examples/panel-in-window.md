# パネル埋め込み

`paneLayout` + `modelPanel` でビューポート付きウィンドウ。

```python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import maya.cmds as cmds

WINDOW_NAME = "panelInWindow"


def deleteWindowIfExists():
    if cmds.window(WINDOW_NAME, exists=True):
        cmds.deleteUI(WINDOW_NAME, window=True)


def show():
    deleteWindowIfExists()
    cmds.window(WINDOW_NAME, title="Viewport Window", widthHeight=(640, 480), sizeable=True)

    rootForm = cmds.formLayout()
    pane = cmds.paneLayout(configuration="single")
    panel = cmds.modelPanel()
    editor = cmds.modelPanel(panel, query=True, modelEditor=True)
    cmds.modelEditor(editor, edit=True, displayAppearance="smoothShaded")

    toolbar = cmds.columnLayout(adjustableColumn=True, rowSpacing=4)
    cmds.button(label="Frame All", command=lambda *_: cmds.viewFit(editor))
    cmds.setParent("..")

    cmds.formLayout(
        rootForm,
        edit=True,
        attachForm=[
            (toolbar, "top", 4),
            (toolbar, "left", 4),
            (toolbar, "right", 4),
            (pane, "left", 4),
            (pane, "right", 4),
            (pane, "bottom", 4),
        ],
        attachControl=[(pane, "top", 4, toolbar)],
        attachNone=[(toolbar, "bottom")],
    )

    cmds.showWindow(WINDOW_NAME)


show()
```

## ポイント

- `modelPanel` の戻り値から `modelEditor` を query し、表示設定・`viewFit` に使う  
- `paneLayout` の `configuration` で分割数を指定（`vertical2` でアウトライナ併設も可）  
- パネルは重いため、必要な場合のみ埋め込む

### アウトライナ併設（vertical2）

```python
pane = cmds.paneLayout(configuration="vertical2")
cmds.outlinerPanel()
cmds.modelPanel()
cmds.paneLayout(pane, edit=True, paneSize=(1, 25, 75))
```
