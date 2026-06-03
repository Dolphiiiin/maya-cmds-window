# メニュー・ポップアップ

`menuBar` + `menuItem` と `popupMenu` の例。

```python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import maya.cmds as cmds

WINDOW_NAME = "menusPopupWindow"


def deleteWindowIfExists():
    if cmds.window(WINDOW_NAME, exists=True):
        cmds.deleteUI(WINDOW_NAME, window=True)


def onAbout(*_):
    cmds.confirmDialog(title="About", message="cmds menu example", button=["OK"])


def onPopupRefresh(*_):
    cmds.inViewMessage(amg="<hl>Refreshed</hl>", pos="midCenter", fade=True)


def show():
    deleteWindowIfExists()
    cmds.window(
        WINDOW_NAME,
        title="Menus Example",
        widthHeight=(280, 160),
        menuBar=True,
    )

    fileMenu = cmds.menu(label="File")
    cmds.menuItem(label="About", command=onAbout)
    cmds.menuItem(divider=True)
    cmds.menuItem(label="Quit", command=lambda *_: deleteWindowIfExists())

    cmds.columnLayout(adjustableColumn=True, rowSpacing=8)
    cmds.optionMenu(label="Quality")
    cmds.menuItem(label="Low")
    cmds.menuItem(label="High")

    targetBtn = cmds.button(label="Right-click me")
    popup = cmds.popupMenu(button=3, parent=targetBtn)
    cmds.menuItem(label="Refresh", command=onPopupRefresh)

    cmds.showWindow(WINDOW_NAME)


show()
```

## ポイント

- `window(..., menuBar=True)` でメニューバー有効化  
- `optionMenu` は layout 内、`menu` はメニューバー用  
- `popupMenu` の `button=3` は右クリック
