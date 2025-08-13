# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import subprocess
import shutil
import tempfile
import textwrap
from pathlib import Path
import sys

TYPST_HEADER = textwrap.dedent("""\
        #set page( paper: "a4", margin: auto )
        #set text(font: "Noto Sans CJK JP", size: 11pt)
""")

TYPST_CHECKLIST_MARKER = "□"


def is_executable() -> bool:
    """
    typst があるかどうか
    """
    return shutil.which("typst") is not None


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


def create_header_checklist(items: list[str], out: Path | None = None) -> Path:
    """
    チェックリスト作った PDF を ./build に作ってその Path を報告する
    """
    content = make_checklist(items)
    if out is None:
        with tempfile.NamedTemporaryFile(
            suffix=".pdf", dir="./build", delete=False
        ) as tmp:
            out = Path(tmp.name)
    gen_pdf(content, out)
    return out


if __name__ == "__main__":
    out = create_header_checklist(sys.argv[1:])
    print(f"output written to {out}")
