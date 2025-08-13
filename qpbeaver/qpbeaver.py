# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import argparse
from pathlib import Path
import tempfile

from qpbeaver.split import process as process_split
from qpbeaver.build import process as process_build

DEFAULT_OUT_DIR: Path = (Path(__file__).parent.parent / "data" / "pdfs").resolve()
DEFAULT_BUILD_DIR: Path = (Path(__file__).parent.parent / "out").resolve()


def do_split(args):
    process_split(args.source, args.pages_data, args.out_dir)


def do_build(args):
    if args.out is None:
        (_, out) = tempfile.mkstemp(
            suffix=".pdf", prefix="qpb_", dir=str(DEFAULT_BUILD_DIR)
        )
    else:
        out = args.out
    process_build(args.source_dir, args.build_directive, out)


def run():
    parser = argparse.ArgumentParser(prog="qpbeaver")

    subparsers = parser.add_subparsers(dest="subcmd")

    # subcommand: split
    split_parser = subparsers.add_parser("split", help="Split")
    split_parser.add_argument(
        "--source",
        "-s",
        type=Path,
        required=True,
        help="PDF file containing pages to split",
    )
    split_parser.add_argument(
        "--pages-data",
        "-p",
        type=Path,
        required=True,
        help="\n".join(
            [
                "Pages and names",
                "\tcomma-separated file that has (name, pages) in each row",
                "\t(see README.md)",
            ]
        ),
    )
    split_parser.add_argument(
        "--out-dir",
        "-o",
        type=Path,
        required=False,
        default=DEFAULT_OUT_DIR,
        help="\n".join(
            [
                "Output directory for resulting files.",
                "\tdefault: data/pdfs in the directory of the script",
            ],
        ),
    )
    split_parser.set_defaults(func=do_split)

    # subcommand: build
    build_parser = subparsers.add_parser("build", help="Build")
    build_parser.add_argument(
        "--source-dir",
        "-s",
        type=Path,
        required=False,
        default=DEFAULT_OUT_DIR,
        help="\n".join(
            [
                "The directory containing files that are split.",
                "\tdefault: data/pdfs in the directory of the script",
            ]
        ),
    )
    build_parser.add_argument(
        "--build-directive",
        "-b",
        type=Path,
        required=True,
        help="Text (csv) file containing pdfs to merge",
    )
    build_parser.add_argument(
        "--out",
        "-o",
        type=Path,
        required=False,
        help="Output file. Default: a randomely-named file under ./out/",
    )
    build_parser.set_defaults(func=do_build)

    args = parser.parse_args()
    if args.subcmd is not None:
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    run()
