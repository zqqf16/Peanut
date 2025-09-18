"""Utility helpers used across Peanut."""

from __future__ import annotations

import re
from os import PathLike
from pathlib import Path
from typing import Iterator, Optional, Sequence, Tuple, TypeVar, Union
from urllib.parse import urljoin, urlsplit
from urllib.request import pathname2url, url2pathname

PathStr = Union[str, PathLike[str]]
T = TypeVar("T")


def to_s(value: object) -> str:
    """Return a string representation for logging/console output."""
    return str(value)


def to_u(value: object) -> str:
    """Backward compatible unicode helper; identical to to_s on Python 3."""
    return str(value)


def path_to_url(path: PathStr) -> str:
    """Convert a filesystem path to a URL-compatible string."""
    return pathname2url(str(path))


def url_to_path(url: str) -> str:
    """Convert a URL-encoded string back to a filesystem path."""
    return url2pathname(url)


def url_safe(value: str) -> str:
    """Normalise a string for use inside URLs."""
    cleaned = re.sub(r"[<>,~!#&{}()\[\]*^$?]", " ", value)
    return "-".join(part for part in cleaned.strip().split())


def real_url(base: str, url: str) -> str:
    """Compose an absolute URL from a base URL and a local path."""
    path = urlsplit(base).path
    if not path.endswith("/"):
        path = f"{path}/"
    relative = url.lstrip("/")
    return urljoin(path, relative)


def package_resource(path: PathStr) -> Path:
    """Return an absolute path to a resource shipped inside the package."""
    return (Path(__file__).resolve().parent / path).resolve()


def neighborhood(items: Sequence[T]) -> Iterator[Tuple[Optional[T], T, Optional[T]]]:
    """Yield (prev, current, next) triples while iterating over *items*."""
    if not items:
        return

    last_index = len(items) - 1
    for index, current in enumerate(items):
        prev_item = items[index - 1] if index > 0 else None
        next_item = items[index + 1] if index < last_index else None
        yield prev_item, current, next_item


def list_dir(path: PathStr) -> Iterator[str]:
    """Yield all non-hidden files under *path* sorted alphabetically."""
    directory = Path(path)
    for entry in sorted(directory.iterdir()):
        if entry.name.startswith(".") or entry.is_dir():
            continue
        yield str(entry)


def get_resource(relative_path: PathStr) -> Path:
    """Return the absolute path of a resource bundled with Peanut."""
    return package_resource(relative_path)

