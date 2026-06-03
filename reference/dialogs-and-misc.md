# ダイアログ・その他 UI

`window` ベースのツール UI 以外の、通知・進捗・HUD・ホットキー等。

---

## モーダルダイアログ

### confirmDialog

[confirmDialog](https://help.autodesk.com/cloudhelp/JPN/MayaCRE-Tech-Docs/CommandsPython/confirmDialog.html)

```python
result = cmds.confirmDialog(
    title="Confirm",
    message="Delete selected nodes?",
    button=["Yes", "No"],
    defaultButton="Yes",
    cancelButton="No",
)
if result == "Yes":
    pass
```

### promptDialog

[promptDialog](https://help.autodesk.com/cloudhelp/JPN/MayaCRE-Tech-Docs/CommandsPython/promptDialog.html)

```python
cmds.promptDialog(title="Rename", message="New name:", button=["OK", "Cancel"])
if cmds.promptDialog(query=True, button=True) == "OK":
    newName = cmds.promptDialog(query=True, text=True)
```

### framelessDialog / layoutDialog

フレームレスまたはレイアウト編集用ダイアログ。

---

## 進捗

### progressWindow

[progressWindow](https://help.autodesk.com/cloudhelp/JPN/MayaCRE-Tech-Docs/CommandsPython/progressWindow.html)

ループ処理と併用。0 件なら開かない。

```python
itemCount = len(nodeList)
if itemCount == 0:
    return

cmds.progressWindow(
    title="Processing",
    progress=0,
    maxValue=itemCount,
    isInterruptable=True,
)

for index, node in enumerate(nodeList):
    if cmds.progressWindow(query=True, isCancelled=True):
        break
    cmds.progressWindow(edit=True, progress=index + 1, status=node)
    # 処理 ...

cmds.progressWindow(endProgress=True)
```

ウィンドウ内の `progressBar` とは別。埋め込み進捗には `progressBar` を layout に配置。

---

## ビューポート・ステータス通知

### inViewMessage

[inViewMessage](https://help.autodesk.com/cloudhelp/JPN/MayaCRE-Tech-Docs/CommandsPython/inViewMessage.html)

ビューポート中央付近への一時メッセージ。

```python
cmds.inViewMessage(
    amg="<hl>Done</hl>",
    pos="midCenter",
    fade=True,
)
```

### headsUpMessage / headsUpDisplay

HUD へのメッセージ・表示要素。アニメーション作業中のオーバーレイ向け。

---

## UI 読み込み・プリファレンス

| コマンド | 用途 |
|----------|------|
| `loadUI` | .ui 実行時読み込み（本リポジトリの変換スキルでは **出力に使わない**。参考: [loadui-mapping-reference.md](../maya-qt-ui-to-cmds/reference/loadui-mapping-reference.md)） |
| `loadPrefObjects` / `savePrefObjects` | UI プリファレンス |
| `savePrefs` | 設定保存 |
| `callbacks` | UI コールバック管理 |

cmds のみで構築する場合は `loadUI` より **Python で layout を組む** 方が一般的。既存 `.ui` からの移行は [maya-qt-ui-to-cmds](../maya-qt-ui-to-cmds/SKILL.md) を参照。

---

## ホットキー

| コマンド | 用途 |
|----------|------|
| `hotkey` | ホットキー定義 |
| `hotkeyCheck` | 競合チェック |
| `hotkeyCtx` | ホットキーコンテキスト |
| `hotkeySet` | ホットキーセット |

---

## その他

| コマンド | 用途 |
|----------|------|
| `annotate` | ビュー注釈 |
| `grabColor` | スポイト |
| `nameCommand` / `runTimeCommand` | 名前付きコマンド |
| `mayaDpiSetting` | DPI 設定 |
| `setStartupMessage` | 起動メッセージ |
| `disableIncorrectNameWarning` | 命名警告の抑制 |

---

## editor / createEditor / editorTemplate

Maya 組み込みエディタとテンプレート。`window` 実行後に uiTemplate を設定する流れと関連（[window-lifecycle.md](window-lifecycle.md)）。

---

## 全コマンド

その他 UI 31 コマンド — [commands-index.md](commands-index.md)
