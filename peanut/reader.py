"""Markdown reader utilities."""

from __future__ import annotations

import datetime as dt
import logging
import re
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

import markdown

from peanut.meta_yaml import MetaYamlExtension


def parser_list(value: Any) -> List[Any]:
    if isinstance(value, list):
        return value
    return [value]


def parser_single(value: Any) -> Any:
    if isinstance(value, list):
        return value[0]
    return value


def parser_bool(value: Any) -> bool:
    candidate = parser_single(value)
    if isinstance(candidate, bool):
        return candidate
    return str(candidate).lower() in {"true", "yes", "1"}


def parser_date(value: Any) -> dt.datetime:
    if isinstance(value, dt.datetime):
        return value
    if isinstance(value, dt.date):
        return dt.datetime.combine(value, dt.time.min)

    date_string = parser_single(value)
    for pattern in ("%Y-%m-%d", "%Y%m%d", "%Y-%m-%d %H:%M", "%Y%m%d %H:%M"):
        try:
            return dt.datetime.strptime(str(date_string), pattern)
        except ValueError:
            continue
    return dt.datetime.now()


class Singleton(type):
    _instances: Dict[type, "MarkdownReader"] = {}

    def __call__(cls, *args: Any, **kwargs: Any):  # type: ignore[override]
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class Reader:
    """Base reader class."""

    regex: Optional[re.Pattern[str]] = None

    def read(self, path: Path | str) -> Optional[Dict[str, Any]]:
        raise NotImplementedError


class MarkdownReader(Reader, metaclass=Singleton):
    """Markdown reader."""

    regex = re.compile(r"([^/]+)\.(md|markdown)$", re.IGNORECASE)

    _meta_parser = {
        "tags": parser_list,
        "category": parser_single,
        "date": parser_date,
        "publish": parser_bool,
        "top": parser_bool,
        "image": parser_single,
    }

    def __init__(self) -> None:
        self.md_parser = self._create_markdown_parser()

    @staticmethod
    def _create_markdown_parser() -> markdown.Markdown:
        extensions: Iterable[Any] = (
            "markdown.extensions.fenced_code",
            "markdown.extensions.codehilite",
            "markdown.extensions.footnotes",
            "markdown.extensions.tables",
            "markdown.extensions.toc",
            MetaYamlExtension(),
        )
        extension_configs = {"codehilite": {"guess_lang": False}}
        return markdown.Markdown(
            extensions=extensions,
            extension_configs=extension_configs,
        )

    @property
    def parser(self) -> markdown.Markdown:
        return self.md_parser.reset()

    def parse_meta(self, meta: Dict[str, Any]) -> Dict[str, Any]:
        parsed: Dict[str, Any] = {}
        for key, value in meta.items():
            parser = self._meta_parser.get(key, lambda v: v)
            parsed[key] = parser(value)
        return parsed

    def read(self, path: Path | str) -> Optional[Dict[str, Any]]:
        file_path = Path(path)
        if not file_path.is_file():
            return None

        file_name = file_path.stem
        result: Dict[str, Any] = {"slug": file_name}

        draft = file_path.read_text(encoding="utf-8")
        content = self.parser.convert(draft.strip(" \n"))

        result.update({"content": content, "raw": self.md_parser.Raw})
        if self.md_parser.Meta:
            new_meta = self.parse_meta(self.md_parser.Meta)
            result["title"] = new_meta.pop("title", file_name)
            result["meta"] = new_meta

        return result


def reader_for_file(path: Path | str) -> Optional[Reader]:
    file_name = Path(path).name
    for cls in Reader.__subclasses__():
        pattern = cls.regex
        if pattern and pattern.match(file_name):
            logging.debug("Find reader %s", cls)
            return cls()
    return None


def read(path: Path | str) -> Optional[Dict[str, Any]]:
    reader = reader_for_file(path)
    if not reader:
        logging.debug("No reader found for file %s", path)
        return None
    return reader.read(path)

