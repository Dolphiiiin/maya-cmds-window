# .ui ファイル構造（Qt Designer XML）

変換前に XML を読むための要点。形式は Qt UI file version 4.0。

## ルート構造

```xml
<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>Dialog</class>
 <widget class="QDialog" name="Dialog">
  <property name="windowTitle">...</property>
  <layout class="QVBoxLayout" name="verticalLayout">
   <item>
    <widget class="QPushButton" name="runButton">
     <property name="text"><string>Run</string></property>
    </widget>
   </item>
  </layout>
 </widget>
 <connections/>
 <customwidgets/>
</ui>
```

| 要素 | 意味 |
|------|------|
| `<class>` | uic が生成する Python クラス名 |
| `<widget>` | ルートウィジェット。`class` が Qt 型、`name` が objectName |
| `<layout>` | 子の配置。widget 直下または item 内 |
| `<property>` | ウィジェット属性。`name` がプロパティ名 |
| `<connections>` | シグナル／スロット（手動リライト時は `command` へ） |
| `<customwidgets>` | カスタム Qt プラグイン（cmds では要代替設計） |

## 階層の読み方

1. ルート `<widget>` の `class` と `name` を記録（→ `cmds.window`）  
2. 直下の `<layout>` を記録（→ `columnLayout` 等）  
3. `<item>` 内の `<widget>` を深さ優先で走査  
4. 各 widget の `name` を cmds UI 名の候補にする  
5. `<spacer>` はマージンまたは `separator` で代替  

## connections の例

```xml
<connections>
 <connection>
  <sender>runButton</sender>
  <signal>clicked()</signal>
  <receiver>Dialog</receiver>
  <slot>accept()</slot>
 </connection>
</connections>
```

cmds への写し方:

| Qt | cmds |
|----|------|
| `clicked()` → カスタムスロット | `cmds.button(..., command=handler)` |
| `clicked()` → `accept()` | `command` 内で `deleteUI` または処理後に閉じる |
| `textChanged(QString)` | `textField` には直接なし。変更検知は別設計（ボタンで確定等） |

## 動的プロパティ（入力の読み取り）

Designer の `+command` / `-command` は、もともと loadUI 向けの指定である。本スキルでは **入力からコールバック意図を読むだけ**で、出力では次の形にする。

```python
def onClick(*_):
    pass

cmds.button("mybutton", command=onClick)
```

`.ui` 内の `+command` 文字列をそのまま実行時 eval しない。

## pyside-uic 出力との対応

`setupUi` 内の `self.runButton = QtWidgets.QPushButton(...)` は、上記 `<widget name="runButton">` と 1:1。  
`self.verticalLayout.addWidget(...)` は `<layout class="QVBoxLayout">` の子追加に対応。

## 解析コマンド

```bash
python maya-qt-ui-to-cmds/scripts/parse_ui_outline.py dialog.ui
```

ツリーと推奨 cmds を Markdown で出力する。
