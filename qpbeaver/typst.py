# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import subprocess
import tempfile
import textwrap
from pathlib import Path
import sys

TYPST_HEADER = textwrap.dedent("""\
        #set page( paper: "a4", margin: auto )
        #set text(font: "Noto Sans CJK JP", size: 11pt)
""")

TYPST_CHECKLIST_MARKER = "□"


def do_typst_compile_pdf(typst_doc: str, out: Path):
    """
    そのまま typst に渡してコンパイルする
    """
    with tempfile.NamedTemporaryFile(suffix=".typ", mode="w", encoding="utf-8") as tmp:
        tmp.write(typst_doc)
        tmp.flush()
        try:
            subprocess.run(["typst", "compile", tmp.name, str(out)], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error compiling file {tmp} with typst: {e}")


def gen_pdf(typst_content: str, out: Path):
    do_typst_compile_pdf(TYPST_HEADER + "\n" + typst_content, out)


def make_checklist(items: list[str]) -> str:
    the_items = ",\n".join((f"[{item}]" for item in items))
    return f"#list(\nmarker:[{TYPST_CHECKLIST_MARKER}],\n" + the_items + "\n)"


def create_header_checklist(items: list[str]) -> Path:
    """
    チェックリスト作った PDF を ./out に作ってその Path を報告する
    """
    with tempfile.NamedTemporaryFile(suffix=".pdf", dir="./out", delete=False) as tmp:
        content = make_checklist(items)
        gen_pdf(content, Path(tmp.name))
        return Path(tmp.name)


if __name__ == "__main__":
    out = create_header_checklist(sys.argv[1:])
    print(f"output written to {out}")
