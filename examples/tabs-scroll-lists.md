# タブ・スクロール・リスト

`tabLayout` と `textScrollList` を組み合わせた選択 UI。

```python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import maya.cmds as cmds

WINDOW_NAME = "tabsScrollListWindow"
LIST_UI = None


def deleteWindowIfExists():
    if cmds.window(WINDOW_NAME, exists=True):
        cmds.deleteUI(WINDOW_NAME, window=True)


def refreshList(*_):
    global LIST_UI
    if LIST_UI is None:
        return
    cmds.textScrollList(LIST_UI, edit=True, removeAll=True)
    nodeList = cmds.ls(type="transform") or []
    for node in sorted(nodeList):
        cmds.textScrollList(LIST_UI, edit=True, append=node)


def onSelect(*_):
    global LIST_UI
    selected = cmds.textScrollList(LIST_UI, query=True, selectItem=True) or []
    if not selected:
        return
    cmds.select(selected, replace=True)


def show():
    global LIST_UI
    deleteWindowIfExists()
    cmds.window(WINDOW_NAME, title="Tabs and Lists", widthHeight=(360, 280))

    tabs = cmds.tabLayout(innerMarginWidth=6, innerMarginHeight=6)

    tabList = cmds.columnLayout(adjustableColumn=True, rowSpacing=6)
    cmds.rowLayout(numberOfColumns=2, columnWidth2=(120, 120))
    cmds.button(label="Refresh", command=refreshList)
    cmds.button(label="Select", command=onSelect)
    cmds.setParent("..")
    LIST_UI = cmds.textScrollList(numberOfRows=12, allowMultiSelection=True)
    cmds.setParent("..")

    tabHelp = cmds.columnLayout(adjustableColumn=True)
    cmds.text(label="Refresh: rebuild list from scene.", align="left")
    cmds.text(label="Select: select highlighted items.", align="left")
    cmds.setParent("..")

    cmds.tabLayout(
        tabs,
        edit=True,
        tabLabel=[(tabList, "Nodes"), (tabHelp, "Help")],
    )

    refreshList()
    cmds.showWindow(WINDOW_NAME)


show()
```

## ポイント

- `tabLayout` の子 layout を `tabLabel` でラベル付け  
- `textScrollList` は `append` / `removeAll` / `selectItem` で操作  
- リスト UI 名はモジュール変数で保持（コールバックから参照）
