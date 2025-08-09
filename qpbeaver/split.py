# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import subprocess
import csv
from pathlib import Path
import re


def validate_pages_string(pages: str) -> str:
    """
    checks if the string is well-formatted for qpdf
    (but we'll ignore complex specifications, especially exclude syntaxes)
    from man qpdf:
        - <n>        where <n> represents a number is the <n>th page
        - r<n>       is the <n>th page from the end
        - z          the last page, same as r1
        - a,b,c      pages a, b, and c
        - a-b        pages a through b inclusive; if a > b, this counts down
    """
    patterns: list[re.Pattern[str]] = [
        re.compile(pat)
        for pat in [
            r"^\d+(,\d+)*$",  # list of pages (or single)
            r"^r\d+$",  # r<n> (nth page from end)
            r"^z$",  # z (last page)
            r"^\d+-\d+$",  # range
        ]
    ]
    if any((pattern.match(pages) for pattern in patterns)):
        return pages
    else:
        raise ValueError(f"Cannot understand pages pattern: {pages}")


def split_pdf(source: Path, name: str, pages: str, out_dir: Path) -> None:
    """
    Split PDF using qpdf command.

    source: source pdf
    name: name to the resulting pdf
    pages: page specification for qpdf
    out_dir: output directory
    """
    output_file = out_dir / f"{name}.pdf"

    # Build qpdf command
    cmd = ["qpdf", "--empty", "--pages", str(source), pages, "--", str(output_file)]

    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"Created: {output_file}")
    except subprocess.CalledProcessError as e:
        print(
            f"Error creating {output_file}: in running {cmd}: \noutput is {e.output}\n stderr was{e.stderr}"
        )
        raise (e)
