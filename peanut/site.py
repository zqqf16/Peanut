"""Site orchestration logic for Peanut."""

from __future__ import annotations

import logging
import shutil
from pathlib import Path
from typing import Iterable, Optional

import peanut.reader as reader
import peanut.writer as writer
from peanut.context import get_filters
from peanut.ghost import get_token, push
from peanut.model import Post
from peanut.options import configs, load_configs, verify_configs
from peanut.template import Template
from peanut.utils import get_resource, list_dir


class Site:
    """Manage Peanut site generation and publication."""

    default_config: Iterable[str] = (
        "_config.yaml",
        "config.yaml",
        "_config.yml",
        "config.yml",
    )

    def __init__(self, directory: Path | str = ".") -> None:
        resolved = Path(directory).resolve()
        logging.debug("Directory is %s", resolved)

        self.curdir: Path = resolved
        self.posts: list[Post] = []
        self.template: Optional[Template] = None

    @staticmethod
    def init(directory: Path | str = ".") -> None:
        """Initialise a Peanut workspace with default assets."""
        target_dir = Path(directory).resolve()

        config_path = target_dir / "config.yml"
        if config_path.is_file():
            logging.error("Config file %s already exists", config_path, prefix="   ↳  ")
            return

        shutil.copy(get_resource("config.yml"), config_path)
        logging.info(
            "Config file created at %s",
            config_path,
            prefix="   ↳  ",
        )

        assets_path = target_dir / "assets"
        if assets_path.exists():
            logging.error("Asset directory %s already exists", assets_path, prefix="   ↳  ")
            return

        shutil.copytree(get_resource("themes/default/assets"), assets_path)
        logging.info(
            "Asset directory created at %s",
            assets_path,
            prefix="   ↳  ",
        )

        draft_path = target_dir / "drafts"
        if draft_path.exists():
            logging.info("Draft directory already exists", prefix="   ↳  ")
            return

        try:
            draft_path.mkdir(parents=True, exist_ok=False)
        except OSError:
            logging.error("Create draft directory failed")
        else:
            logging.info(
                "Draft directory created at %s", draft_path, prefix="   ↳  "
            )

    def load_config(self, config_path: Optional[str]) -> None:
        """Load configuration from *config_path* or default locations."""
        configs.pwd = str(self.curdir)
        candidate: Optional[str] = config_path

        if not candidate:
            logging.debug("No config path is specified, try default ones")
            for file_name in self.default_config:
                potential = self.curdir / file_name
                if potential.is_file():
                    logging.debug("Find config file named %s", file_name)
                    candidate = file_name
                    break
            else:
                logging.debug("Config file with default names not found")
                raise FileNotFoundError(
                    f"Config file not found at directory {self.curdir}"
                )
        else:
            potential = self.curdir / candidate
            if not potential.is_file():
                logging.debug("%s is not a file", candidate)
                raise FileNotFoundError(f"Config file not found at path {candidate}")

        logging.debug("Load config file %s", candidate)
        load_configs(candidate)

        logging.info("Verifing configurations...")
        verify_configs()

        self.template = Template(
            configs.theme_path,
            filters=get_filters(configs),
            site=configs.site,
            author=configs.author,
        )

    def load_drafts(self) -> None:
        """Load all drafts from the configured directory."""
        draft_dir = Path(configs.pwd) / configs.path.draft
        for draft_file in list_dir(draft_dir):
            logging.visiable("Reading %s", draft_file)
            self.parse_draft(draft_file)

    def parse_draft(self, draft_file: str) -> None:
        """Parse a draft file and append it to the in-memory post list."""
        draft = reader.read(draft_file)
        if not draft:
            logging.visiable("Failed", prefix="   ✗  ")
            return

        title = draft.get("title")
        slug = draft.get("slug")
        if not title or not slug:
            logging.visiable("✗ No title or slug", prefix="   ↳  ")
            return

        if not draft["meta"].get("publish", True):
            logging.visiable("✗ Don't publish", prefix="   ↳  ")
            return

        post = Post(
            title,
            slug,
            draft.get("raw"),
            draft.get("content"),
            draft.get("meta"),
        )

        self.posts.append(post)
        logging.visiable("✓ %s", post.title, prefix="   ↳  ")

    def push(self, url: str, username: str, password: str) -> None:
        """Push posts to a Ghost server."""
        logging.info("Loading drafts...")
        self.load_drafts()
        self.posts.sort(reverse=True)

        logging.info("Getting token...")
        token = get_token(url, username, password)
        if not token:
            return

        push(url, token, self.posts)
        logging.info("%d posts", len(self.posts), prefix="🎉  ")

    def generate(self) -> None:
        """Generate the static site."""
        logging.info("Loading drafts...")
        self.load_drafts()
        self.posts.sort(reverse=True)

        writers = [
            (writer.PostWriter, "posts"),
            (writer.TagWriter, "tags"),
            (writer.PageWriter, "index"),
        ]

        if configs.rss:
            writers.append((writer.RssWriter, "rss"))
        if configs.sitemap:
            writers.append((writer.SitemapWriter, "sitemap"))
        if configs.archive:
            writers.append((writer.ArchiveWriter, "archive"))

        logging.info("Rendering files...")
        for writer_class, description in writers:
            logging.visiable(description)
            writer_instance = writer_class(posts=self.posts, template=self.template)
            writer_instance.run()

        logging.info("%d posts", len(self.posts), prefix="🎉  ")
