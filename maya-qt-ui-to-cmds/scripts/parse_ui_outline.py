# -*- coding: utf-8 -*-
# Copyright 2026 COYOTE 3DCG STUDIO Technical Department
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Qt Designer .ui を解析し、cmds 変換アウトラインを Markdown で出力"""
from __future__ import absolute_import, division, print_function

import argparse
import os
import sys
import xml.etree.ElementTree as ElementTree

# 手動リライト用の推奨 cmds（widget-mapping.md と同期）
WIDGET_TO_CMDS = {
    "QDialog": "window",
    "QMainWindow": "window",
    "QWidget": "window",
    "QVBoxLayout": "columnLayout",
    "QHBoxLayout": "rowLayout",
    "QGridLayout": "gridLayout",
    "QFormLayout": "formLayout",
    "QGroupBox": "frameLayout",
    "QTabWidget": "tabLayout",
    "QScrollArea": "scrollLayout",
    "QFrame": "frameLayout",
    "QLabel": "text",
    "QPushButton": "button",
    "QToolButton": "button",
    "QLineEdit": "textField",
    "QTextEdit": "scrollField",
    "QPlainTextEdit": "scrollField",
    "QComboBox": "optionMenu",
    "QCheckBox": "checkBox",
    "QRadioButton": "radioButton",
    "QSpinBox": "intField",
    "QDoubleSpinBox": "floatField",
    "QSlider": "intSlider",
    "QListWidget": "textScrollList",
    "QTreeWidget": "treeView",
    "QProgressBar": "progressBar",
}

UNSUPPORTED_NOTE = {
    "QDialogButtonBox": "個別 QPushButton + rowLayout へ分解",
    "QSpacerItem": "layout マージンまたは separator",
}


def getPropertyText(widgetElement, propertyName):
    """widget 直下の property から string テキスト取得"""
    for prop in widgetElement.findall("property"):
        if prop.get("name") != propertyName:
            continue
        stringEl = prop.find("string")
        if stringEl is not None and stringEl.text:
            return stringEl.text
    return None


def getSuggestedCmds(qtClass):
    """Qt クラス名から推奨 cmds コマンド"""
    if qtClass in WIDGET_TO_CMDS:
        return WIDGET_TO_CMDS[qtClass]
    if qtClass in UNSUPPORTED_NOTE:
        return "({})".format(UNSUPPORTED_NOTE[qtClass])
    return "要調査（widget-mapping.md）"


def walkWidget(widgetElement, depth, lines):
    """widget ツリーを再帰走査"""
    qtClass = widgetElement.get("class", "")
    objectName = widgetElement.get("name", "")
    indent = "  " * depth
    suggested = getSuggestedCmds(qtClass)
    labelText = getPropertyText(widgetElement, "text")
    titleText = getPropertyText(widgetElement, "windowTitle")
    extra = ""
    if labelText:
        extra = " text={!r}".format(labelText)
    if titleText:
        extra = " title={!r}".format(titleText)

    lines.append(
        "{}- **{}** `{}` → `{}`{}".format(indent, qtClass, objectName, suggested, extra)
    )

    layoutEl = widgetElement.find("layout")
    if layoutEl is not None:
        layoutClass = layoutEl.get("class", "QLayout")
        layoutName = layoutEl.get("name", "")
        layoutCmd = getSuggestedCmds(layoutClass)
        lines.append(
            "{}  - layout **{}** `{}` → `{}`".format(
                indent, layoutClass, layoutName, layoutCmd
            )
        )
        for item in layoutEl.findall("item"):
            childWidget = item.find("widget")
            if childWidget is not None:
                walkWidget(childWidget, depth + 1, lines)
            spacer = item.find("spacer")
            if spacer is not None:
                spacerName = spacer.get("name", "spacer")
                lines.append(
                    "{}  - spacer `{}` → separator / margin".format(indent, spacerName)
                )


def parseConnections(rootUi, lines):
    """connections セクションを出力"""
    connections = rootUi.find("connections")
    if connections is None:
        return
    items = connections.findall("connection")
    if not items:
        return
    lines.append("")
    lines.append("## シグナル / スロット（cmds では command へ置換）")
    lines.append("")
    for conn in items:
        sender = conn.find("sender")
        signal = conn.find("signal")
        receiver = conn.find("receiver")
        slot = conn.find("slot")
        lines.append(
            "- `{}` **{}** → `{}` **{}**".format(
                sender.text if sender is not None else "?",
                signal.text if signal is not None else "?",
                receiver.text if receiver is not None else "?",
                slot.text if slot is not None else "?",
            )
        )


def buildOutline(uiPath):
    """.ui を解析して Markdown 文字列を返す"""
    tree = ElementTree.parse(uiPath)
    rootUi = tree.getroot()
    rootWidget = rootUi.find("widget")
    if rootWidget is None:
        return "# Error\n\nNo root <widget> in ui file.\n"

    lines = [
        "# UI 変換アウトライン",
        "",
        "ソース: `{}`".format(uiPath),
        "",
        "## ウィジェット階層（推奨 cmds）",
        "",
    ]
    walkWidget(rootWidget, 0, lines)
    parseConnections(rootUi, lines)
    lines.append("")
    lines.append("## 次のステップ")
    lines.append("")
    lines.append("1. 未対応 Qt クラスを [widget-mapping.md](../reference/widget-mapping.md) で確認")
    lines.append("2. [conversion-workflow.md](../reference/conversion-workflow.md) に従い cmds 手書きコードを生成")
    lines.append("3. 出力に loadUI / PySide / Qt を含めない（[SKILL.md](../SKILL.md)）")
    lines.append("4. 例: [manual-rewrite-dialog.md](../examples/manual-rewrite-dialog.md)")
    lines.append("")
    return "\n".join(lines)


def main():
    """エントリポイント"""
    parser = argparse.ArgumentParser(description=".ui から cmds 変換アウトラインを生成")
    parser.add_argument("ui_file", help=".ui ファイルパス")
    parser.add_argument(
        "-o",
        "--output",
        help="出力 Markdown パス（省略時は標準出力）",
    )
    args = parser.parse_args()
    uiPath = os.path.abspath(args.ui_file)
    if not os.path.isfile(uiPath):
        sys.stderr.write("File not found: {}\n".format(uiPath))
        sys.exit(1)

    markdown = buildOutline(uiPath)
    if args.output:
        with open(args.output, "w") as handle:
            handle.write(markdown)
        print("Wrote {}".format(args.output))
    else:
        print(markdown)


if __name__ == "__main__":
    main()
