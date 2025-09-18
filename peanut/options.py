"""Project configuration management for Peanut."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Mapping

import yaml


class ValidationError(Exception):
    """Raised when configuration values fail validation."""

    def __init__(self, msg: str | None = None) -> None:
        super().__init__(msg)
        self.msg = msg


class LoadingError(ValidationError):
    """Raised when configuration files cannot be parsed."""

    pass


class Option(dict):
    """Dictionary wrapper allowing attribute-style access."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.update(*args, **kwargs)

    def __setitem__(self, key: str, value: Any) -> None:
        if isinstance(value, dict) and not isinstance(value, Option):
            value = Option(value)
        super().__setitem__(key, value)

    def __getitem__(self, name: str) -> Any:
        try:
            return super().__getitem__(name)
        except KeyError:
            return None

    def __delitem__(self, name: str) -> None:
        super().__delitem__(name)

    __getattr__ = __getitem__
    __setattr__ = __setitem__

    def __real_update(self, key: str, value: Any) -> None:
        current = self.get(key)
        if isinstance(current, Option) and isinstance(value, Mapping):
            current.update(value)
        else:
            self[key] = value

    def update(self, *args: Any, **kwargs: Any) -> None:  # type: ignore[override]
        if args:
            if len(args) > 1:
                raise TypeError(
                    f"update expected at most 1 arguments, got {len(args)}"
                )
            mapping = dict(args[0])
            for key, value in mapping.items():
                self.__real_update(key, value)

        for key, value in kwargs.items():
            self.__real_update(key, value)


configs = Option(
    {
        "pwd": str(Path.cwd()),
        "site": {
            "title": "Peanut",
            "logo": None,
            "cover": None,
            "url": "http://peanut.zorro.im",
            "description": "Another peanut blog",
            "navigation": False,
        },
        "author": {
            "image": None,
            "name": "Your Name",
            "url": "/posts/about.html",
            "bio": None,
            "location": "Beijing, China",
        },
        "path": {
            "draft": "drafts",
            "post": "posts/{slug}.html",
            "tag": "tags/{title}/",
            "pagination": "page/{num}/",
            "index": "index.html",
            "sitemap": "sitemap.xml",
            "rss": "rss.xml",
            "asset": "/assets/",
            "archive": "archive.html",
        },
        "sitemap": True,
        "rss": True,
        "archive": True,
        "theme": "default",
        "theme_path": "",
        "pagination": 10,
    }
)


def verify_path() -> None:
    """Verify path configurations."""

    draft = Path(configs.pwd) / configs.path.draft
    if not draft.is_dir():
        raise ValidationError(f"Draft path {draft} not found")

    site_url = str(configs.site.url)
    if not site_url.startswith(("http://", "https://")):
        configs.site.url = f"http://{site_url}"


def verify_theme() -> None:
    """Verify theme configurations."""

    theme = configs.theme
    if not theme:
        raise ValidationError("Theme name must be provided")

    post = "post.html"
    index = "index.html"

    local_path = Path(configs.pwd) / theme
    if local_path.is_dir():
        for template in (post, index):
            if not (local_path / template).is_file():
                raise ValidationError(
                    f"Template for {template} not found in theme {theme}"
                )

        configs.theme_path = str(local_path)
        return

    package_path = Path(__file__).resolve().parent
    theme_path = package_path / "themes" / theme
    if not theme_path.is_dir():
        raise ValidationError(f"Theme named {theme} not found")

    configs.theme_path = str(theme_path)


def verify_configs() -> None:
    for verify_func in (verify_path, verify_theme):
        verify_func()


def load_yaml(path: Path | str) -> Mapping[str, Any]:
    """Load YAML format config file."""

    config_file = Path(path)
    if not config_file.exists():
        raise LoadingError(f"Config file {config_file} not found")

    with config_file.open("r", encoding="utf-8") as stream:
        data = yaml.safe_load(stream)

    if data is None:
        return {}
    if not isinstance(data, Mapping):
        raise LoadingError("Configuration file must contain a mapping at the top level")
    return data


def load_configs(path: str) -> None:
    """Load configs from path."""

    config_path = Path(configs.pwd) / path
    suffix = config_path.suffix.lower()

    if suffix in (".yml", ".yaml"):
        config_yaml = load_yaml(config_path)
        if config_yaml:
            configs.update(config_yaml)
        else:
            logging.debug("Config file is empty")
    else:
        raise LoadingError(f"Unsupported config file type {suffix}")


env = Option({
    "posts": [],
})

