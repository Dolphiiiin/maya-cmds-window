# loadUI マッピング参考（出力禁止）

**このドキュメントは調査用である。変換結果の Python コードに `cmds.loadUI` を書いてはならない。**

Maya が Qt Designer のウィジェットをどの cmds コマンドに対応付けるかを理解するための参考。手動リライト時のマッピング確認に使う。

公式: [loadUI](https://help.autodesk.com/cloudhelp/JPN/MayaCRE-Tech-Docs/CommandsPython/loadUI.html)

## エージェント向けルール

| 用途 | 可否 |
|------|------|
| Qt クラス名 → cmds コマンドの調査 | 可（本ページ、`listTypes`） |
| 変換後コードで `.ui` を実行時読み込み | **不可** |
| 変換後コードに `loadUI(...)` を出力 | **不可** |

## Maya 内で対応表を取得（調査のみ）

```python
import maya.cmds as cmds

# 調査用。返値をマッピング表の補足に使う。出力コードには含めない。
cmds.loadUI(listTypes=True)
```

## loadUI の挙動（なぜ出力に使わないか）

| 事項 | 内容 |
|------|------|
| layout | 汎用 `layout` のみ。`columnLayout` / `formLayout` の専用 API が使えない |
| 未対応 widget | Qt のまま残り cmds から触れない（例: `QDialogButtonBox`） |
| query / edit | loadUI 自体は query / edit 不可 |
| 実行時依存 | `.ui` ファイルパスが残り、PySide/Qt パイプラインと混在しやすい |

手書き cmds なら `columnLayout` / `formLayout` を明示でき、配布物から `.ui` を外せる。

## 代表的な対応（参考）

手動リライトでは [widget-mapping.md](widget-mapping.md) を正とする。loadUI の認識とおおむね一致する例:

| Qt | cmds（手書き出力） |
|----|-------------------|
| `QDialog` | `window` |
| `QVBoxLayout` | `columnLayout` |
| `QHBoxLayout` | `rowLayout` |
| `QPushButton` | `button` |
| `QLabel` | `text` |
| `QLineEdit` | `textField` |
| `QComboBox` | `optionMenu` |
| `QCheckBox` | `checkBox` |
| `QGroupBox` | `frameLayout` |
| `QTabWidget` | `tabLayout` |

バージョン差があるため、疑問時は `listTypes` で確認し、**出力は常に手書き cmds** とする。

## 旧ドキュメント

以前の `loadui.md`（loadUI をブリッジ戦略として紹介）は廃止。本ファイルに統合した。
