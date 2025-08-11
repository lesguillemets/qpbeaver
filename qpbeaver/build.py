# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import subprocess
import csv
from pathlib import Path
from typing import TypeVar

from qpbeaver.typst import create_header_checklist


def merge_pdfs(files: list[Path], out: Path):
    """
    与えられた PDF をまとめる
    """
    cmd = ["qpdf", "--empty", "--pages"]
    cmd += [str(f) for f in files]
    cmd += ["--", str(out)]
    subprocess.run(cmd, check=True)
    print(f"Created: {out}")


def process(
    source_dir: Path, build_directive: Path, out: Path, append_toc: bool = True
):
    """
    build_directives: csv file in the format of
    name(, optionally + name to use in toc)

    the program will look for `{name}.pdf` in the source_dir,
    and the name will be used in the toc.
    If you want to use another name, add it in the second column.
    """
    directives = read_directive(build_directive)
    files: list[Path] = []
    names: list[str] = []
    for name, toc_name in directives:
        names.append(toc_name or name)  # if toc_name is not None, use that
        pdf = search_pdf(source_dir, name)
        if not pdf:
            raise FileNotFoundError(f"Cannot find {name}.pdf in {source_dir}")
        files.append(pdf)
    if append_toc:
        toc: Path = create_header_checklist(names)
        files.append(toc)

    merge_pdfs(files, out)
    print(f"Created: {out}")
    if append_toc and toc.is_file():
        toc.unlink()


def search_pdf(source_dir: Path, name: str) -> Path | None:
    """
    search for a pdf in the source_dir, allowing case-insensitive search.
    """
    for pdf in source_dir.rglob("*.pdf", case_sensitive=False):
        if pdf.stem.lower() == name.lower():
            return pdf
    return None


def read_directive(build_directive: Path) -> list[tuple[str, str | None]]:
    """
    parses pages data from a csv
    returns: a list of tuples (name, pages).
    """
    with open(build_directive, "r") as f:
        reader = csv.reader(f, delimiter=",")
        return [(row[0], safe_get(row, 1)) for row in reader if row]


T = TypeVar("T")


def safe_get(row: list[T], idx: int) -> T | None:
    try:
        return row[idx]
    except IndexError:
        return None
