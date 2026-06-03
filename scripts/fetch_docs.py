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
"""cat_Windows HTML から commands-index.md を再生成するメンテ用スクリプト"""
from __future__ import absolute_import, division, print_function

import argparse
import os
import re
import sys

try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen

DOC_BASE = "https://help.autodesk.com/cloudhelp/JPN/MayaCRE-Tech-Docs/CommandsPython/"
CAT_WINDOWS_URL = DOC_BASE + "cat_Windows.html"

SECTION_HEADERS = [
    ("window", "## ウィンドウ"),
    ("panel", "## パネル"),
    ("control", "## コントロール"),
    ("layout", "## レイアウト"),
    ("menu", "## メニュー"),
    ("other", "## その他UI"),
]

LINK_PATTERN = re.compile(
    r"\[([a-zA-Z][a-zA-Z0-9]*)\]\(javascript:go%28'([a-zA-Z0-9]+)\.html'%29\)"
)
SECTION_PATTERN = re.compile(r"^## (.+)$", re.MULTILINE)


def fetchUrl(url):
    """URL から HTML テキスト取得"""
    response = urlopen(url)
    raw = response.read()
    if sys.version_info[0] >= 3:
        return raw.decode("utf-8", errors="replace")
    return raw


def parseSections(htmlText):
    """HTML/Markdown からカテゴリ別コマンド名リストを抽出"""
    sectionMap = {}
    currentKey = None
    keyByTitle = {
        "ウィンドウ": "window",
        "パネル": "panel",
        "コントロール": "control",
        "レイアウト": "layout",
        "メニュー": "menu",
        "その他UI": "other",
    }
    for line in htmlText.splitlines():
        if line.startswith("## "):
            title = line[3:].strip()
            currentKey = keyByTitle.get(title)
            if currentKey and currentKey not in sectionMap:
                sectionMap[currentKey] = []
            continue
        if currentKey:
            for match in LINK_PATTERN.finditer(line):
                cmdName = match.group(1)
                if cmdName not in sectionMap[currentKey]:
                    sectionMap[currentKey].append(cmdName)
    return sectionMap


def buildIndexMarkdown(sectionMap):
    """commands-index.md 本文生成"""
    lines = [
        "# cmds ウィンドウ API コマンド索引",
        "",
        "出典: [cat_Windows]({})".format(CAT_WINDOWS_URL),
        "",
        "各コマンドの詳細は公式ページ `{name}.html` を参照。",
        "",
    ]
    for key, header in SECTION_HEADERS:
        cmdList = sectionMap.get(key, [])
        lines.append(header)
        lines.append("")
        lines.append("| コマンド | 公式 URL |")
        lines.append("|--------|----------|")
        for cmdName in sorted(cmdList):
            url = DOC_BASE + cmdName + ".html"
            lines.append("| `{}` | [{}]({}) |".format(cmdName, cmdName, url))
        lines.append("")
        lines.append("合計: {} コマンド".format(len(cmdList)))
        lines.append("")
    total = sum(len(sectionMap.get(k, [])) for k, _ in SECTION_HEADERS)
    lines.append("---")
    lines.append("")
    lines.append("**全カテゴリ合計**: {} コマンド".format(total))
    lines.append("")
    return "\n".join(lines)


def main():
    """エントリポイント"""
    parser = argparse.ArgumentParser(description="commands-index.md を再生成")
    parser.add_argument(
        "--input",
        help="ローカル cat_Windows HTML/MD パス（省略時は公式 URL を取得）",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="出力先（既定: reference/commands-index.md）",
    )
    args = parser.parse_args()
    scriptDir = os.path.dirname(os.path.abspath(__file__))
    repoRoot = os.path.dirname(scriptDir)
    outputPath = args.output or os.path.join(repoRoot, "reference", "commands-index.md")

    if args.input:
        with open(args.input, "r") as handle:
            htmlText = handle.read()
    else:
        htmlText = fetchUrl(CAT_WINDOWS_URL)

    sectionMap = parseSections(htmlText)
    markdown = buildIndexMarkdown(sectionMap)
    outputDir = os.path.dirname(outputPath)
    if outputDir and not os.path.isdir(outputDir):
        os.makedirs(outputDir)

    with open(outputPath, "w") as handle:
        handle.write(markdown)

    print("Wrote {}".format(outputPath))
    for key, _ in SECTION_HEADERS:
        count = len(sectionMap.get(key, []))
        print("  {}: {}".format(key, count))


if __name__ == "__main__":
    main()
