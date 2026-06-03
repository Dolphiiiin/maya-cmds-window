# パネル

ビューポート、アウトライナ、ハイパーグラフ等の **エディタパネル** をウィンドウ内に埋め込むコマンド群。

全コマンド: [commands-index.md](commands-index.md) のパネル節。

---

## 典型構成

```
window
  └── formLayout / columnLayout
        └── paneLayout
              ├── modelPanel
              └── outlinerPanel（任意）
```

[panel-in-window 例](../examples/panel-in-window.md) を参照。

---

## modelPanel / modelEditor

| コマンド | 役割 |
|----------|------|
| `modelPanel` | モデルビューの **パネル** UI（layout 子） |
| `modelEditor` | パネル内の **エディタ** 設定（カメラ、表示オプション） |

[modelPanel](https://help.autodesk.com/cloudhelp/JPN/MayaCRE-Tech-Docs/CommandsPython/modelPanel.html)

```python
pane = cmds.paneLayout(configuration="single")
panel = cmds.modelPanel()
editor = cmds.modelPanel(panel, query=True, modelEditor=True)
cmds.modelEditor(editor, edit=True, displayAppearance="smoothShaded")
```

---

## outlinerPanel / outlinerEditor

シーン階層表示。`modelPanel` と `paneLayout` で左右分割する構成が多い。

```python
pane = cmds.paneLayout(configuration="vertical2")
top = cmds.outlinerPanel()
bottom = cmds.modelPanel()
cmds.paneLayout(pane, edit=True, paneSize=(1, 30, 70))
```

---

## paneLayout

[paneLayout](https://help.autodesk.com/cloudhelp/JPN/MayaCRE-Tech-Docs/CommandsPython/paneLayout.html)

| フラグ | 用途 |
|--------|------|
| `configuration` | `single`, `vertical2`, `horizontal2`, `quad` 等 |
| `paneSize` | ペイン比率 |

---

## その他エディタパネル

| コマンド | 用途 |
|----------|------|
| `hyperGraph` / `hyperPanel` | ノードグラフ |
| `hyperShade` | シェーディングネットワーク |
| `nodeEditor` | ノードエディタ |
| `spreadSheetEditor` | スプレッドシート |
| `componentEditor` | コンポーネント |
| `hardwareRenderPanel` | ハードウェアレンダ |
| `scriptedPanel` | スクリプト定義パネル |
| `webBrowser` | 内蔵ブラウザ |

---

## panel / getPanel / setFocus

| コマンド | 用途 |
|----------|------|
| `panel` | パネル作成・編集 |
| `getPanel` | 現在のパネル情報取得 |
| `setFocus` | パネルへフォーカス |
| `panelConfiguration` / `panelHistory` | レイアウト構成 |

---

## scriptedPanel / scriptedPanelType

カスタムパネルタイプの登録。高度な統合向け。

---

## 注意点

- パネルは **通常の button より重い**。不要なら `modelPanel` 1 枚で十分か検討  
- パネル名は Maya セッション内で一意性が必要な場合がある  
- ウィンドウ `deleteUI` 時にパネルもまとめて破棄される（`retain` の挙動に注意）  
- `saveViewportSettings` でビューポート設定を保存可能  

---

## 関連

- レイアウト: [layouts.md](layouts.md) の `paneLayout`  
- ウィンドウ: [window-lifecycle.md](window-lifecycle.md)
