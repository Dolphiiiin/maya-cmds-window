# ウィンドウライフサイクル

`window` カテゴリの中核コマンドと、ツール UI 構築で頻出する周辺コマンド。

公式ベース: [window](https://help.autodesk.com/cloudhelp/JPN/MayaCRE-Tech-Docs/CommandsPython/window.html)

UI クラス・VERSION・シーン切替は [tool-conventions.md](tool-conventions.md) を正とする。

## window

新しいウィンドウを作成する。作成直後は **非表示**。子を追加したあと `showWindow` で表示するのが効率的。

### 重要な挙動

| 事項 | 内容 |
|------|------|
| 非表示作成 | `visible` は既定で false 相当。`showWindow` まで表示されない |
| layout 必須 | ボタン等の control はウィンドウ直下に置けない。layout が必要 |
| uiTemplate | `window` 実行で **uiTemplate スタックがクリア**される。テンプレートは window 後に設定 |
| 閉じると削除 | 既定では閉じると UI が削除される。`retain=True` で保持 |

### 主要フラグ

| フラグ | 用途 |
|--------|------|
| `title` | タイトルバー表示文字列（`self.WINDOW_TITLE`） |
| `widthHeight` | クライアント領域の幅・高さ（ピクセル） |
| `sizeable` | ユーザーによるリサイズ可否 |
| `resizeToFitChildren` | 子 control に合わせてウィンドウサイズ調整 |
| `modal` | モーダル（他ウィンドウ入力をブロック） |
| `retain` | 閉じた後も UI オブジェクトを保持 |
| `closeCommand` | 閉じた後に実行するスクリプト（`self.onClose`） |
| `menuBar` | 空のメニューバーを追加 |
| `toolbox` | ツールボックススタイル（Windows） |
| `exists` | 照会: 指定名のウィンドウが存在するか |

### UI クラス + 単一インスタンス

```python
import maya.cmds as cmds


class MyToolWindow(object):
    WINDOW_NAME = "myToolWindow"
    VERSION = "1.0.0"
    WINDOW_TITLE = "{} v{}".format(WINDOW_NAME, VERSION)

    def __init__(self):
        self.reopenOnSceneChange = True
        self.sceneScriptJobIdList = []

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

    def onClose(self, *_):
        self.removeSceneReopenCallbacks()
        self.deleteWindowIfExists()

    def buildUi(self):
        cmds.window(
            self.WINDOW_NAME,
            title=self.WINDOW_TITLE,
            widthHeight=(320, 200),
            sizeable=True,
            closeCommand=self.onClose,
        )
        cmds.columnLayout(adjustableColumn=True)
        cmds.button(label="Run", command=self.onRun)

    def onRun(self, *_):
        pass

    def show(self):
        self.deleteWindowIfExists()
        self.buildUi()
        self.installSceneReopenCallbacks()
        cmds.showWindow(self.WINDOW_NAME)


_myToolWindow = None


def showToolWindow():
    global _myToolWindow
    if _myToolWindow is None:
        _myToolWindow = MyToolWindow()
    _myToolWindow.show()
```

## showWindow

[showWindow](https://help.autodesk.com/cloudhelp/JPN/MayaCRE-Tech-Docs/CommandsPython/showWindow.html)

ウィンドウを可視化する。引数省略時は **直近に作成した window** が対象。アイコン化中なら復元する。

```python
cmds.showWindow(self.WINDOW_NAME)
```

## deleteUI

UI 要素の削除。ウィンドウ全体は `deleteUI(name, window=True)`。

```python
cmds.deleteUI(self.WINDOW_NAME, window=True)
```

## toggleWindowVisibility / windowPref

| コマンド | 用途 |
|----------|------|
| `toggleWindowVisibility` | 表示・非表示の切り替え |
| `windowPref` | ウィンドウ位置・サイズのプリファレンス保存 |

## ダイアログ系（独立ウィンドウ）

`window` + layout とは別系統。モーダル確認や入力に使う。

| コマンド | 用途 |
|----------|------|
| `confirmDialog` | OK / Cancel 等の確認 |
| `promptDialog` | テキスト入力 |
| `progressWindow` | 進捗バー付き処理（ループと併用） |
| `layoutDialog` | レイアウト編集ダイアログ |
| `colorEditor` / `fontDialog` | 色・フォント選択 |

詳細は [dialogs-and-misc.md](dialogs-and-misc.md)。

## メインウィンドウ操作

Maya メインウィンドウ名は MEL グローバル `$gMainWindow`。

```python
import maya.mel as mel

mainWindow = mel.eval("$tmp=$gMainWindow")
cmds.window(mainWindow, edit=True, widthHeight=(1200, 800))
```

## control（共通）

[control](https://help.autodesk.com/cloudhelp/JPN/MayaCRE-Tech-Docs/CommandsPython/control.html)

任意の UI control の **編集・照会** に使う。control 名は `self` に保持する。

```python
cmds.control(self.runButton, edit=True, enable=False)
```

## setParent

レイアウト階層の移動。`'..'` で親 layout に戻る。

```python
cmds.setParent("..")
```

## 関連コマンド（索引）

`window`, `showWindow`, `deleteUI` ほか — 全一覧は [commands-index.md](commands-index.md)。
