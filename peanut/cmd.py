"""Peanut command line interface."""

from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import Optional

from docopt import docopt

import peanut
from peanut import site
from peanut.logger import init_logger

USAGE = """Peanut

Usage:
  peanut init [(-v|-d)] [<directory>]
  peanut ghost <url> <username> <password>
  peanut [(-v|-d)] [-c | --config <config_file_path>] [<directory>]
  peanut (-h | --help)
  peanut --version

Options:
  -c --config   Config file path.
  -v            Visible logging output.
  -d            Show debug logs.
  -h --help     Show help.
  --version     Show version.
"""


def _resolve_directory(directory: Optional[str]) -> str:
    return str(Path(directory or "./").resolve())


def main() -> None:
    args = docopt(USAGE, version=f"Peanut {peanut.__version__}")

    directory = _resolve_directory(args.get("<directory>"))
    config_path = args.get("<config_file_path>")

    visible = args.get("-v", False)
    debug = args.get("-d", False)

    if debug:
        init_logger(logging.DEBUG)
    elif visible:
        init_logger(logging.VISIABLE)
    else:
        init_logger(logging.INFO)

    if args["init"]:
        logging.info("Init peanut environments")
        site.Site.init(directory)
        sys.exit(0)

    blog = site.Site(directory)

    logging.info("Loading configurations...")
    try:
        blog.load_config(config_path)
    except Exception as exc:  # pragma: no cover - CLI error path
        logging.critical(str(exc))
        sys.exit(-1)

    if args["ghost"]:
        url = args.get("<url>")
        user = args.get("<username>")
        password = args.get("<password>")
        if not url or not user or not password:
            logging.critical("Invalid arguments")
            sys.exit(-1)
        blog.push(url, user, password)
        sys.exit(0)

    logging.info("Generating...")
    blog.generate()


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    main()

