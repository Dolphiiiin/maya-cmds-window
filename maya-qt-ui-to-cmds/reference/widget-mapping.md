# Qt ウィジェット → cmds 対応表

`.ui` / `Ui_*` を **cmds 手書きコードに変換**するときの対応表。出力に PySide / Qt / `loadUI` は含めない。

マッピングの補足調査のみ [loadui-mapping-reference.md](loadui-mapping-reference.md) を参照。

## レイアウト

| Qt クラス | cmds（出力コード） |
|-----------|-------------------|
| `QVBoxLayout` | `columnLayout` |
| `QHBoxLayout` | `rowLayout` |
| `QGridLayout` | `gridLayout` |
| `QFormLayout` | `formLayout` または label + field の `columnLayout` |
| `QStackedLayout` | `tabLayout` または複数 frame の出し分け |
| `QSpacerItem` | `separator` または layout マージン |

## ウィンドウ・コンテナ

| Qt クラス | cmds（出力） | 備考 |
|-----------|-------------|------|
| `QDialog` | `window` | `modal=True` でモーダル |
| `QMainWindow` | `window` + `menuBar` / `formLayout` | ツールバーは `toolBar` または button 行 |
| `QWidget`（ルート） | `window` | 子用に layout 必須 |
| `QGroupBox` | `frameLayout`（`label` = タイトル） | |
| `QTabWidget` | `tabLayout` | 各タブは子 layout |
| `QScrollArea` | `scrollLayout` + 子 `columnLayout` | `childResizable=True` |
| `QFrame` | `frameLayout` または `separator` | `HLine` / `VLine` は `separator` |
| `QSplitter` | `paneLayout` または `formLayout` | 比率は attach で再現 |

## 入力・表示

| Qt クラス | cmds | プロパティ対応の目安 |
|-----------|------|---------------------|
| `QLabel` | `text` | `text` → `label` |
| `QPushButton` | `button` | `text` → `label` |
| `QToolButton` | `button` または `symbolButton` | |
| `QLineEdit` | `textField` | `text` → `text` |
| `QTextEdit` / `QPlainTextEdit` | `scrollField` | 複数行 |
| `QComboBox` | `optionMenu` + `menuItem` | 項目は `addItem` 相当で append |
| `QCheckBox` | `checkBox` | `text` → `label` |
| `QRadioButton` | `radioButton` + `radioCollection` | グループは collection |
| `QSpinBox` | `intField` | min / max / value |
| `QDoubleSpinBox` | `floatField` | |
| `QSlider` | `intSlider` / `floatSlider` | 向きは `rowLayout` で配置 |
| `QListWidget` | `textScrollList` | 複雑なセルは cmds では再設計 |
| `QTreeWidget` | `treeView` | データ供給 API が異なる |
| `QTableWidget` | `scriptTable` | または簡略化して list 化 |
| `QProgressBar` | `progressBar` | |

## 未対応・要注意（cmds 化）

| Qt クラス | 問題 | 推奨代替 |
|-----------|------|----------|
| `QDialogButtonBox` | cmds に相当なし | `rowLayout` + 個別 `button` |
| `QDateEdit` / `QTimeEdit` | cmds に直接なし | `textField` + バリデーション |
| `QFontComboBox` | なし | `optionMenu` または `fontDialog` 呼び出し |
| `QWebEngineView` | なし | `webBrowser` パネル検討 |
| `QGraphicsView` | なし | `canvas` または機能削減 |
| カスタム `QWidget` サブクラス | なし | 機能を cmds control に分解 |

## プロパティ・コールバック

| Qt / Designer | cmds 出力 |
|---------------|----------|
| `objectName` | UI 名（`window` / control 名）。一意にする |
| `text` / `title` | `label` / `title` |
| `enabled` | `enable` |
| `visible` | `visible` |
| `toolTip` | `annotation` |
| `clicked()` 等シグナル | `command=callable` |
| Designer 動的プロパティ `+command` / `-command` | 入力の意図を読み取り、出力では Python 関数を `command=` に渡す |

シグナル／スロットは cmds に存在しない。`command` / `closeCommand` / 専用フラグで置き換える。

## スタイル

| Qt | cmds |
|----|------|
| `styleSheet` (CSS) | 再現不可。`backgroundColor` 等、限られたフラグのみ |
| アイコン (`icon` property) | `image` / `iconTextButton` で部分的に可能 |
| フォント | ほぼ不可 |

見た目の完全一致は期待しない。機能同等を優先する。

## sizePolicy / 最小サイズ

Qt の `sizePolicy` は cmds にない。リサイズ追従は親 `formLayout` の attach で再現する（[maya-cmds-window layouts](../../reference/layouts.md)）。
