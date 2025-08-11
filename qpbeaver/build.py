# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import subprocess
import csv
from pathlib import Path
from typing import TypeVar


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
    pass


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
