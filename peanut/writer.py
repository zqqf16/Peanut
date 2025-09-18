"""Writers responsible for rendering output artifacts."""

from __future__ import annotations

import logging
from collections import defaultdict
from pathlib import Path
from typing import Iterator, MutableMapping, Sequence

from peanut.model import Pagination, Post, Tag
from peanut.options import configs
from peanut.template import Template


class Writer:
    """Base writer."""

    def __init__(self, posts: Sequence[Post], template: Template) -> None:
        self.posts: list[Post] = list(posts)
        self.template = template

    def write_to_file(self, file_path: str | Path, content: str) -> None:
        target = (Path(configs.pwd) / Path(file_path)).resolve()
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")

    def run(self) -> None:  # pragma: no cover - defined by subclasses
        raise NotImplementedError


class PostWriter(Writer):
    """Render individual posts."""

    def run(self) -> None:
        for post in self.posts:
            logging.debug("Render post %s", post.title)
            content = self.render(post)
            logging.debug("Write to %s", post.file_path, prefix="   ↳  ")
            self.write_to_file(post.file_path, content)

    def render(self, post: Post) -> str:
        prev_post, next_post = self._get_post_neighbor(post)
        return self.template.render(
            post.layout,
            post=post,
            prev_post=prev_post,
            next_post=next_post,
        )

    def _get_post_neighbor(self, post: Post) -> tuple[Post | None, Post | None]:
        index = self.posts.index(post)
        prev_post = self.posts[index - 1] if index > 0 else None
        next_post = self.posts[index + 1] if index < len(self.posts) - 1 else None
        return prev_post, next_post


class PageWriter(Writer):
    """Render paginated index-like pages."""

    def __init__(
        self,
        posts: Sequence[Post],
        template: Template,
        layout: str | None = None,
        base_url: str | None = None,
    ) -> None:
        super().__init__(posts, template)
        self.base_url = base_url or configs.path.index
        self.layout = layout or "index"
        self.num_per_page = configs.pagination
        self.context: dict[str, object] = {}

    def run(self, posts: Sequence[Post] | None = None) -> None:
        current_posts = list(posts) if posts is not None else self.posts
        page = Pagination(
            current_posts,
            base_url=self.base_url,
            posts_per_page=self.num_per_page,
        )

        for pagination in page.iterate():
            content = self.render(pagination)
            logging.debug("Write file %s", pagination.file_path, prefix="   ↳  ")
            self.write_to_file(pagination.file_path, content)

    def render(self, page: Pagination) -> str:
        return self.template.render(
            self.layout,
            posts=page.posts,
            page=page,
            prev_page=page.prev,
            next_page=page.next,
            **self.context,
        )


class ArchiveWriter(Writer):
    """Render archive pages grouped by year."""

    def __init__(self, posts: Sequence[Post], template: Template) -> None:
        super().__init__(posts, template)
        self.layout = "archive"
        self.file_path = configs.path["archive"]

    def run(self) -> None:
        content = self.render()
        self.write_to_file(self.file_path, content)

    def render(self) -> str:
        years = list(self.posts_per_year())
        return self.template.render(self.layout, years=years)

    def posts_per_year(self) -> Iterator[list[Post]]:
        if not self.posts:
            return
        current_year = self.posts[0].date.year
        bucket: list[Post] = []
        for post in self.posts:
            if post.date.year != current_year:
                yield bucket
                bucket = []
                current_year = post.date.year
            bucket.append(post)
        if bucket:
            yield bucket


class TagWriter(PageWriter):
    """Render tag listing pages."""

    def __init__(self, posts: Sequence[Post], template: Template) -> None:
        super().__init__(posts, template, "tag", configs.path.tag)
        self.tags: MutableMapping[Tag, list[Post]] = defaultdict(list)
        for post in posts:
            for tag in post.tags:
                self.tags[tag].append(post)

    def run(self) -> None:
        for tag, tag_posts in self.tags.items():
            logging.debug("Render tag %s", tag.title)
            if not tag_posts:
                continue
            self.context["tag"] = tag
            self.base_url = tag.file_path
            super().run(posts=tag_posts)


class RssWriter(Writer):
    """Render RSS feeds."""

    def __init__(self, posts: Sequence[Post], template: Template, layout: str = "rss") -> None:
        super().__init__(posts, template)
        self.file_path = configs.path[layout]
        self.layout = layout
        self.num = 5

    def run(self) -> None:
        logging.debug("Render %s", self.file_path)
        content = self.render()
        logging.debug("Write file %s", self.file_path)
        self.write_to_file(self.file_path, content)

    def render(self) -> str:
        return self.template.render(self.layout, posts=self.posts[: self.num])


class SitemapWriter(RssWriter):
    """Render sitemap XML."""

    def __init__(self, posts: Sequence[Post], template: Template) -> None:
        super().__init__(posts, template, "sitemap")
        self.num = len(self.posts)

