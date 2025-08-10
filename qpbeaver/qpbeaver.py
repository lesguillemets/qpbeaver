# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import argparse
from pathlib import Path

from qpbeaver.split import process as process_split


def do_split(args):
    process_split(args.source, args.pages_data, args.out_dir)


def do_build(args):
    print("Build:")
    print(f"--source-dir: {args.source_dir}")
    print(f"--build-directive: {args.build_directive}")
    print(f"--out: {args.out}")


def run():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers()

    # subcommand: split
    split_parser = subparsers.add_parser("split", help="Split")
    split_parser.add_argument(
        "--source", "-s", type=Path, required=True, help="Process this file"
    )
    split_parser.add_argument(
        "--pages-data", "-p", type=Path, required=True, help="Pages and names"
    )
    split_parser.add_argument(
        "--out-dir",
        "-o",
        type=Path,
        required=True,
        help="Output directory for resulting files",
    )
    split_parser.set_defaults(func=do_split)

    # subcommand: build
    build_parser = subparsers.add_parser("build", help="Build")
    build_parser.add_argument(
        "--source-dir",
        "-s",
        type=Path,
        required=True,
        help="The directory containing files that are split",
    )
    build_parser.add_argument(
        "--build-directive",
        "-b",
        type=Path,
        required=True,
        help="How do I assemble the files",
    )
    build_parser.add_argument(
        "--out", "-o", type=Path, required=True, help="Output file"
    )
    build_parser.set_defaults(func=do_build)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    run()
