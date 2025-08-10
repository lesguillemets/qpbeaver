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


if __name__ == "__main__":
    with tempfile.NamedTemporaryFile(suffix=".pdf", dir="./data", delete=False) as f:
        gen_pdf("\n".join(sys.argv[1:]), Path(f.name))
        print(f"output written to {f.name}")
