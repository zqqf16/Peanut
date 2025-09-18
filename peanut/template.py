"""Template utilities built on top of Jinja2."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional

import jinja2
from jinja2 import ChoiceLoader, FileSystemLoader
from jinja2.exceptions import TemplateNotFound

from peanut.utils import get_resource


class SmartLoader(FileSystemLoader):
    """FileSystemLoader that can resolve templates without extensions."""

    available_extension = (".html", ".xml")

    def get_source(self, environment: jinja2.Environment, template: str):  # type: ignore[override]
        if template is None:
            raise TemplateNotFound(template)
        if "." in template:
            return super().get_source(environment, template)

        for extension in SmartLoader.available_extension:
            filename = f"{template}{extension}"
            try:
                return super().get_source(environment, filename)
            except TemplateNotFound:
                continue
        raise TemplateNotFound(template)


class Template:
    """Wrapper around Jinja2 environment with Peanut defaults."""

    def __init__(self, path: str | Path, filters: Optional[Dict[str, Any]] = None, **kwargs: Any) -> None:
        search_paths = [str(Path(path)), str(get_resource("themes/default"))]
        loader = ChoiceLoader([SmartLoader(p) for p in search_paths])
        self.env = jinja2.Environment(
            loader=loader,
            lstrip_blocks=True,
            trim_blocks=True,
        )
        if isinstance(filters, dict):
            self.env.filters.update(filters)

        self.env.globals.update(kwargs)

    def update_context(self, **kwargs: Any) -> None:
        self.env.globals.update(kwargs)

    def render(self, name: str, **context: Any) -> str:
        template = self.env.get_template(name)
        return template.render(**context)

