"""YAML meta data extension for Python-Markdown."""

from __future__ import annotations

from typing import List

import yaml
from markdown import Extension, Markdown
from markdown.preprocessors import Preprocessor


class MetaYamlExtension(Extension):
    """Extension for parsing YAML metadata blocks."""

    def extendMarkdown(self, md: Markdown) -> None:  # type: ignore[override]
        md.preprocessors.register(MetaYamlPreprocessor(md), "meta_yaml", 25)


class MetaYamlPreprocessor(Preprocessor):
    """Extract YAML metadata from the beginning of a document."""

    def run(self, lines: List[str]) -> List[str]:  # type: ignore[override]
        yaml_block: List[str] = []
        if lines and lines[0] == "---":
            lines.pop(0)
            while lines:
                line = lines.pop(0)
                if line in ("---", "..."):
                    break
                yaml_block.append(line)
        if yaml_block:
            meta = yaml.safe_load("\n".join(yaml_block)) or {}
            meta = {str(k).lower(): v for k, v in meta.items()}
            self.md.Meta = meta
        else:
            self.md.Meta = {}

        self.md.Raw = "\n".join(lines)
        return lines


def makeExtension(configs: dict | None = None) -> MetaYamlExtension:
    """Set up the extension (entry point for markdown)."""

    return MetaYamlExtension(configs=configs or {})

