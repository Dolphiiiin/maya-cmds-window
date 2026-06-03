# レイアウト

UI コンポーネントの配置を担う layout コマンド群。ウィンドウ直下には layout のみ置ける。

## 選定早見表

| 目的 | コマンド |
|------|----------|
| 縦一列 | `columnLayout` |
| 横一列 | `rowLayout` |
| 折り返し配置 | `flowLayout` |
| 絶対・相対配置（リサイズ追従） | `formLayout` |
| 表形式 | `gridLayout` / `rowColumnLayout` |
| スクロール | `scrollLayout` |
| タブ | `tabLayout` |
| 枠付きグループ | `frameLayout` |
| ペイン分割（パネル用） | `paneLayout` |
| ドッキング | `dockControl` |

---

## columnLayout

[columnLayout](https://help.autodesk.com/cloudhelp/JPN/MayaCRE-Tech-Docs/CommandsPython/columnLayout.html)

子 control を縦に並べる。ツール UI の入門に最適。

| フラグ | 用途 |
|--------|------|
| `adjustableColumn` | ウィンドウ幅に合わせて列幅を伸縮 |
| `rowSpacing` | 行間 |
| `columnAttach` | 左右マージン |

```python
cmds.columnLayout(adjustableColumn=True, rowSpacing=6)
cmds.button(label="A")
cmds.button(label="B")
cmds.setParent("..")
```

## rowLayout

[rowLayout](https://help.autodesk.com/cloudhelp/JPN/MayaCRE-Tech-Docs/CommandsPython/rowLayout.html)

子を横一列に配置。`numberOfColumns` と `columnWidth` で列幅を制御。

## formLayout

[formLayout](https://help.autodesk.com/cloudhelp/JPN/MayaCRE-Tech-Docs/CommandsPython/formLayout.html)

子 control のエッジ（top / left / bottom / right）をフォームまたは他 control にアタッチする。リサイズに強い。

### アタッチ種別

| フラグ | 意味 |
|--------|------|
| `attachForm` | フォーム辺に固定（オフセット付き） |
| `attachOppositeForm` | フォームの反対辺に固定 |
| `attachControl` | 別 control の近い辺に固定 |
| `attachOppositeControl` | 別 control の遠い辺に固定 |
| `attachPosition` | フォーム幅に対する比率位置（`numberOfDivisions` 基準、既定 100） |
| `attachNone` | 非アタッチ（control サイズで決まる） |

### 注意

- 各子について **上下左右の各方向に少なくとも 1 エッジ**をアタッチしないと表示されない  
- 子同士の `attachControl` が **循環**すると警告され無視される  

```python
form = cmds.formLayout(numberOfDivisions=100)
btnTop = cmds.button(label="Top")
btnBottom = cmds.button(label="Bottom")
cmds.formLayout(
    form,
    edit=True,
    attachForm=[
        (btnTop, "top", 5),
        (btnTop, "left", 5),
        (btnTop, "right", 5),
        (btnBottom, "left", 5),
        (btnBottom, "right", 5),
        (btnBottom, "bottom", 5),
    ],
    attachControl=[(btnBottom, "top", 5, btnTop)],
    attachNone=[(btnTop, "bottom")],
)
```

複数タプルをリストで渡せる（公式 Python 例参照）。

## frameLayout

[frameLayout](https://help.autodesk.com/cloudhelp/JPN/MayaCRE-Tech-Docs/CommandsPython/frameLayout.html)

ラベル付き枠。`collapsable=True` で折りたたみ可能。

```python
cmds.frameLayout(label="Options", collapsable=True, collapse=False)
cmds.columnLayout(adjustableColumn=True)
cmds.checkBox(label="Verbose")
cmds.setParent("..")
cmds.setParent("..")
```

## scrollLayout

[scrollLayout](https://help.autodesk.com/cloudhelp/JPN/MayaCRE-Tech-Docs/CommandsPython/scrollLayout.html)

子が大きいときにスクロールバーを表示。

```python
scroll = cmds.scrollLayout(childResizable=True)
cmds.columnLayout(adjustableColumn=True)
# 多数の control ...
cmds.setParent("..")
cmds.setParent("..")
```

## tabLayout

[tabLayout](https://help.autodesk.com/cloudhelp/JPN/MayaCRE-Tech-Docs/CommandsPython/tabLayout.html)

タブページ。子 layout をタブごとに作成し、`edit=True` で `selectTabIndex` 等を操作。

```python
tabs = cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=5)
tab1 = cmds.columnLayout()
cmds.text(label="Tab 1 content")
cmds.setParent("..")
tab2 = cmds.columnLayout()
cmds.text(label="Tab 2 content")
cmds.setParent("..")
cmds.tabLayout(
    tabs,
    edit=True,
    tabLabel=[(tab1, "General"), (tab2, "Advanced")],
)
```

## paneLayout

[paneLayout](https://help.autodesk.com/cloudhelp/JPN/MayaCRE-Tech-Docs/CommandsPython/paneLayout.html)

ペイン分割。`modelPanel` や `outlinerPanel` の親として使う。`configuration` で分割数を指定。

## gridLayout / rowColumnLayout / flowLayout

| コマンド | 用途 |
|----------|------|
| `gridLayout` | 固定セル数のグリッド |
| `rowColumnLayout` | 行・列数を指定した表 |
| `flowLayout` | 幅に応じて折り返すフロー配置 |

## dockControl

[dockControl](https://help.autodesk.com/cloudhelp/JPN/MayaCRE-Tech-Docs/CommandsPython/dockControl.html)

Maya ドック領域へ UI をドッキング。ツールを常設パネル化するときに使用。

## layout（汎用）

[layout](https://help.autodesk.com/cloudhelp/JPN/MayaCRE-Tech-Docs/CommandsPython/layout.html)

任意 layout の編集・照会。

## menuBarLayout / shelfLayout / toolBar / workspaceControl

Maya 組み込み UI 向け。カスタムツールでは `columnLayout` / `formLayout` が主。

## 階層の原則

```
window
  └── layout（必須）
        ├── layout / control
        └── frameLayout
              └── columnLayout
                    └── control ...
```

`setParent('..')` を忘れると、以降の control が意図しない親の下に作られる。

## 全コマンド一覧

`columnLayout`, `dockControl`, `flowLayout`, `formLayout`, `frameLayout`, `gridLayout`, `layout`, `menuBarLayout`, `paneLayout`, `rowColumnLayout`, `rowLayout`, `scrollLayout`, `shelfLayout`, `shelfTabLayout`, `tabLayout`, `toolBar`, `workspaceControl`, `workspaceLayoutManager` — [commands-index.md](commands-index.md)
