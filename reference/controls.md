# コントロール

ボタン、フィールド、スライダ、属性連動 UI など。いずれも **親 layout の下**に作成する。

全 81 コマンドの索引: [commands-index.md](commands-index.md) のコントロール節。

---

## ボタン・ラベル

| コマンド | 用途 |
|----------|------|
| `button` | 汎用ボタン |
| `symbolButton` | シンボル表示ボタン |
| `iconTextButton` | アイコン + テキスト |
| `text` | 静的テキスト |
| `separator` | 区切り線 |
| `helpLine` / `messageLine` | ヘルプ・メッセージ行 |

### button

[button](https://help.autodesk.com/cloudhelp/JPN/MayaCRE-Tech-Docs/CommandsPython/button.html)

| フラグ | 用途 |
|--------|------|
| `label` | 表示文字列 |
| `command` | クリック時コールバック（関数推奨） |
| `enable` | 有効 / 無効 |
| `backgroundColor` | 背景色 RGB 0–1 |

```python
def onRun(*_):
    pass

cmds.button(label="Execute", command=onRun)
```

---

## テキスト入力

| コマンド | 用途 |
|----------|------|
| `textField` | 1 行入力 |
| `textFieldGrp` | ラベル付き 1 行 |
| `textFieldButtonGrp` | 入力 + ボタン（ファイル参照等） |
| `scrollField` | 複数行（スクロール） |
| `nameField` | ノード名入力 |

```python
name = cmds.textFieldGrp(
    label="Node",
    text="pCube1",
    buttonLabel="<<",
    buttonCommand=pickFromSelection,
)
value = cmds.textFieldGrp(name, query=True, text=True)
```

---

## 数値・スライダ

| コマンド | 用途 |
|----------|------|
| `intField` / `floatField` | 単体フィールド |
| `intFieldGrp` / `floatFieldGrp` | ラベル付きグループ |
| `intSlider` / `floatSlider` | スライダ単体 |
| `intSliderGrp` / `floatSliderGrp` | ラベル + スライダ + フィールド |
| `floatSliderButtonGrp` | スライダ + ボタン |
| `intScrollBar` / `floatScrollBar` | スクロールバー型 |

```python
slider = cmds.floatSliderGrp(
    label="Weight",
    field=True,
    minValue=0.0,
    maxValue=1.0,
    value=0.5,
    step=0.01,
)
```

---

## 選択 UI

| コマンド | 用途 |
|----------|------|
| `checkBox` / `checkBoxGrp` | オン / オフ |
| `radioButton` + `radioCollection` | 単一選択ラジオ |
| `radioButtonGrp` | ラベル付きラジオグループ |
| `textScrollList` | 文字列リスト（複数選択可） |
| `iconTextScrollList` | アイコン付きリスト |
| `treeView` / `treeLister` / `nodeTreeLister` | ツリー表示 |

### textScrollList

[textScrollList](https://help.autodesk.com/cloudhelp/JPN/MayaCRE-Tech-Docs/CommandsPython/textScrollList.html)

```python
listUi = cmds.textScrollList(
    numberOfRows=8,
    allowMultiSelection=True,
)
cmds.textScrollList(listUi, edit=True, append="item_a")
cmds.textScrollList(listUi, edit=True, append="item_b")
selected = cmds.textScrollList(listUi, query=True, selectItem=True) or []
```

---

## 属性連動（attr*）

ノード属性と UI を接続する高レベル control。

| コマンド | 用途 |
|----------|------|
| `attrFieldGrp` | 属性フィールド |
| `attrFieldSliderGrp` | フィールド + スライダ |
| `attrControlGrp` | 属性タイプに応じた control |
| `attrColorSliderGrp` | カラー属性 |
| `attrNavigationControlGrp` | シーン内ナビゲーション付き |

```python
cmds.attrFieldSliderGrp(
    attribute="pCube1.translateX",
    label="Translate X",
)
```

`connectControl` で任意 control を属性に接続することも可能（[attribute-driven-ui 例](../examples/attribute-driven-ui.md)）。

---

## カラー・グラデーション

`colorSliderGrp`, `colorSliderButtonGrp`, `colorIndexSliderGrp`, `colorInputWidgetGrp`, `gradientControl`, `gradientControlNoAttr`, `palettePort`, `swatchDisplayPort`

---

## 特殊・組み込み向け

| コマンド | 備考 |
|----------|------|
| `channelBox` | チャンネルボックス（Maya 組み込み） |
| `timeControl` / `timePort` | タイムライン系 |
| `progressBar` | ウィンドウ内進捗（`progressWindow` とは別） |
| `canvas` / `image` / `picture` | 描画・画像表示 |
| `scriptTable` | 表形式スクリプト UI |
| `cmdShell` / `commandLine` | コマンドライン系 |

カスタムツールでは **button / field / slider / attr* / textScrollList** が中心。

---

## control 共通操作

任意 control 名に対し:

```python
cmds.control(uiName, edit=True, enable=False)
cmds.control(uiName, edit=True, visible=False)
annotation = cmds.control(uiName, query=True, annotation=True)
```

---

## 命名と重複

- UI 名を省略すると自動生成名が返る。再利用する場合は **明示名**または変数に保持  
- 同じウィンドウ名で再 `window` する前に `deleteUI`  
