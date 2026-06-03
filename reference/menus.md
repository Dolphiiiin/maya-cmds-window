# メニュー

ウィンドウメニューバー、オプションメニュー、ポップアップメニュー。

全コマンド: [commands-index.md](commands-index.md) のメニュー節。

---

## 基本構成

```
window (menuBar=True)
  └── menu
        └── menuItem
        └── menuItem (subMenu=True)
              └── menuItem ...
```

`window` 作成時に `menuBar=True` を指定するか、後から `menu` を追加する。

---

## menu / menuItem

[menu](https://help.autodesk.com/cloudhelp/JPN/MayaCRE-Tech-Docs/CommandsPython/menu.html)  
[menuItem](https://help.autodesk.com/cloudhelp/JPN/MayaCRE-Tech-Docs/CommandsPython/menuItem.html)

| 対象 | 主要フラグ |
|------|------------|
| `menu` | `label`, `tearOff` |
| `menuItem` | `label`, `command`, `divider`, `subMenu`, `radioButton`, `checkBox` |

```python
cmds.window(menuBar=True)
mainMenu = cmds.menu(label="Tool")
cmds.menuItem(label="Run", command=onRun)
cmds.menuItem(divider=True)
cmds.menuItem(label="Close", command=onClose)
```

サブメニュー:

```python
cmds.menuItem(label="Export", subMenu=True)
cmds.menuItem(label="OBJ", command=exportObj)
cmds.menuItem(label="FBX", command=exportFbx)
cmds.setParent("..", menu=True)
```

---

## optionMenu / optionMenuGrp

[optionMenu](https://help.autodesk.com/cloudhelp/JPN/MayaCRE-Tech-Docs/CommandsPython/optionMenu.html)

ドロップダウン選択。layout 内に配置する。

```python
menu = cmds.optionMenu(label="Mode")
cmds.menuItem(label="Fast")
cmds.menuItem(label="Accurate")
cmds.optionMenu(menu, edit=True, select=2)
current = cmds.optionMenu(menu, query=True, value=True)
```

`optionMenuGrp` はラベル付きラッパー。

---

## popupMenu

[popupMenu](https://help.autodesk.com/cloudhelp/JPN/MayaCRE-Tech-Docs/CommandsPython/popupMenu.html)

control へ右クリックメニューをアタッチ。

```python
btn = cmds.button(label="Target")
popup = cmds.popupMenu(button=3, parent=btn)
cmds.menuItem(label="Refresh", command=onRefresh)
```

| フラグ | 用途 |
|--------|------|
| `button` | トリガーボタン（3 = 右クリック） |
| `parent` | 対象 control |

---

## 属性・列挙メニュー

| コマンド | 用途 |
|----------|------|
| `attrEnumOptionMenu` | 列挙属性用 |
| `attrEnumOptionMenuGrp` | ラベル付き |
| `attributeMenu` | 属性選択メニュー |
| `radioMenuItemCollection` | メニュー内ラジオ集合 |

---

## Maya 組み込み・編集系

| コマンド | 用途 |
|----------|------|
| `menuEditor` | メニュー編集 UI |
| `menuSet` / `menuSetPref` | メニューセット |
| `hotBox` | ホットボックス |
| `artBuildPaintMenu` / `saveMenu` | 特化メニュー |

カスタムツールでは `menu` + `menuItem` + `optionMenu` + `popupMenu` が中心。

---

## メニューバーへの optionMenu 配置（メインウィンドウ）

Maya メインウィンドウのメニューバー右上など:

```python
import maya.mel as mel

cmds.setParent("")
menuName = cmds.optionMenu(label="My Menu")
cmds.menuItem(label="Item 1", parent=menuName)
melMain = mel.eval("$tmp=$gMainWindow")
cmds.window(melMain, edit=True, menuBarCornerWidget=(menuName, "topRight"))
```

詳細: [window 公式](https://help.autodesk.com/cloudhelp/JPN/MayaCRE-Tech-Docs/CommandsPython/window.html)。
