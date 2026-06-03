# ツール UI 共通規約

cmds ツールウィンドウ全般に適用する規約。変換スキル [maya-qt-ui-to-cmds](../maya-qt-ui-to-cmds/SKILL.md) の出力もこれに従う。

## UI クラスでまとめる

ウィンドウ構築・状態・コールバックは **1 つの UI クラス**に集約する。モジュール直下に UI 用の関数を散らさない。

| 保持先 | 内容 |
|--------|------|
| クラス定数 | `WINDOW_NAME`, `VERSION`, `WINDOW_TITLE` |
| `self` | シーン開き直しフラグ、scriptJob ID リスト、control 名、ツールパラメータ |

```python
class BasicToolWindow(object):
    WINDOW_NAME = "basicToolWindow"
    VERSION = "1.0.0"
    WINDOW_TITLE = "{} v{}".format(WINDOW_NAME, VERSION)

    def __init__(self):
        self.reopenOnSceneChange = True
        self.sceneScriptJobIdList = []
        self.runButton = None

    def deleteWindowIfExists(self):
        if cmds.window(self.WINDOW_NAME, exists=True):
            cmds.deleteUI(self.WINDOW_NAME, window=True)

    def buildUi(self):
        cmds.window(
            self.WINDOW_NAME,
            title=self.WINDOW_TITLE,
            widthHeight=(240, 120),
            sizeable=True,
            closeCommand=self.onClose,
        )
        cmds.columnLayout(adjustableColumn=True)
        self.runButton = cmds.button(label="Run", command=self.onRun)

    def show(self):
        self.deleteWindowIfExists()
        self.buildUi()
        self.installSceneReopenCallbacks()
        cmds.showWindow(self.WINDOW_NAME)

    def onRun(self, *_):
        pass

    def onClose(self, *_):
        self.removeSceneReopenCallbacks()
        self.deleteWindowIfExists()
```

エントリポイントはモジュール関数 `show()` でインスタンスを保持する。

```python
_toolWindow = None

def show():
    global _toolWindow
    if _toolWindow is None:
        _toolWindow = BasicToolWindow()
    _toolWindow.show()
```

## バージョン定数とタイトル

`WINDOW_NAME` と `VERSION` を定数で定義し、**定数の連結**でタイトル文字列を作る。

```python
WINDOW_NAME = "basicToolWindow"
VERSION = "1.0.0"
WINDOW_TITLE = "{} v{}".format(WINDOW_NAME, VERSION)
```

| 項目 | ルール |
|------|--------|
| 表示形式 | `{WINDOW_NAME} v{VERSION}`（例: `basicToolWindow v1.0.0`） |
| `WINDOW_TITLE` | クラス定数として 1 回だけ連結 |
| `cmds.window` | `title=self.WINDOW_TITLE` |

`WINDOW_TITLE_BASE` は使わない。リリース時は `VERSION`（と `WINDOW_TITLE` の再計算）のみ更新する。

## シーン切り替え時のウィンドウ開き直し

### 目的

シーン依存パラメータの整合性リセットのため、シーン切替時に **UI を破棄して作り直す**。

### 既定（シーン依存ツール）

`self.reopenOnSceneChange = True`（クラス定数でも可）。`self.sceneScriptJobIdList` で job を管理。

```python
def installSceneReopenCallbacks(self):
    self.removeSceneReopenCallbacks()
    if not self.reopenOnSceneChange:
        return
    for eventName in ["NewSceneOpened", "SceneOpened"]:
        jobId = cmds.scriptJob(e=True, event=[eventName, self.onSceneChanged])
        self.sceneScriptJobIdList.append(jobId)

def removeSceneReopenCallbacks(self):
    for jobId in self.sceneScriptJobIdList:
        if cmds.scriptJob(exists=jobId):
            cmds.scriptJob(kill=jobId, force=True)
    self.sceneScriptJobIdList = []

def onSceneChanged(self, *_):
    self.deleteWindowIfExists()
    self.show()
```

`show()` の末尾で `installSceneReopenCallbacks()`。`onClose` で `removeSceneReopenCallbacks()`。

### 例外（シーン横断ツール）

```python
self.reopenOnSceneChange = False  # シーン横断のため開き直しなし
```

`installSceneReopenCallbacks` を呼ばない。理由をクラス docstring またはコメントで残す。

## チェックリスト

- [ ] UI が 1 クラスにまとまっているか  
- [ ] パラメータ・control 名・scriptJob が `self` で保持されているか  
- [ ] `WINDOW_TITLE = "{} v{}".format(WINDOW_NAME, VERSION)` か  
- [ ] シーン依存ツールで `self.reopenOnSceneChange` と scriptJob があるか  
- [ ] 横断ツールで `reopenOnSceneChange = False` と理由があるか  
- [ ] 閉じるときに scriptJob を kill しているか  
