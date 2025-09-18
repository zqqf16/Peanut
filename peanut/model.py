"""Domain models used by Peanut."""

from __future__ import annotations

import posixpath
import re
from datetime import datetime
from typing import Any, Dict, Iterable, List, Optional

from peanut.options import configs
from peanut.utils import path_to_url, real_url, url_safe


class BaseModel:
    """Base model class providing path helpers."""

    layout: Optional[str] = None

    @property
    def file_path(self) -> str:
        template = str(configs.path.get(self.__class__.layout, "")).lstrip("/")
        return url_safe(template.format(**self.__dict__))

    @property
    def url(self) -> str:
        relative_url = path_to_url(self.file_path)
        if not relative_url.startswith("/"):
            relative_url = "/" + relative_url
        return real_url(configs.site.url, relative_url)


class Tag(BaseModel):
    """Tag model."""

    layout = "tag"

    def __init__(self, title: str) -> None:
        self.title = title
        self.slug = url_safe(title)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Tag):
            return NotImplemented
        return self.title == other.title

    def __hash__(self) -> int:
        return hash(self.title)


class Post(BaseModel):
    """Post model."""

    layout = "post"

    def __init__(
        self,
        title: str,
        slug: str,
        raw: Optional[str] = None,
        content: Optional[str] = None,
        meta: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.title = title
        self.slug = url_safe(slug)
        self.content = content
        self.raw = raw

        metadata = dict(meta or {})
        self.date = metadata.pop("date", None) or datetime.now()
        self.publish = metadata.pop("publish", True)
        self.layout = metadata.pop("layout", Post.layout)
        self.top = metadata.pop("top", False)
        self.tag_titles = metadata.pop("tags", [])

        image = metadata.pop("image", None)
        if isinstance(image, dict):
            self.image = image.get("feature")
        else:
            self.image = image

        self.meta = metadata

    @property
    def tags(self) -> List[Tag]:
        return [Tag(title) for title in self.tag_titles]

    def __getattr__(self, key: str) -> Any:
        try:
            return super().__getattribute__(key)
        except AttributeError:
            return self.meta.get(key)

    def __lt__(self, other: "Post") -> bool:
        return self.date < other.date


class Pagination:
    """Pagination helper."""

    def __init__(
        self,
        posts: Iterable[Post],
        page: int = 1,
        base_url: Optional[str] = None,
        posts_per_page: int = 5,
    ) -> None:
        self._posts = list(posts)
        self.page = page
        self.base_url = base_url or ""
        self.posts_per_page = posts_per_page or len(self._posts)

        self.path: Optional[str] = None
        self.url: Optional[str] = None
        self.parse_path_and_url()

    def parse_path_and_url(self) -> None:
        template = configs.path.pagination
        relative_path = template.format(number=self.page, num=self.page, n=self.page)

        if self.page == 1:
            relative_path = ""

        base_url = self.base_url or ""
        if re.search(r"index.html?$", base_url):
            parent, index_name = posixpath.split(base_url)
            url = file_path = posixpath.join(parent, relative_path, index_name)
        else:
            if not base_url.endswith("/"):
                base_url = f"{base_url}/"
            else:
                if relative_path and not relative_path.endswith("/"):
                    relative_path = f"{relative_path}/"
            url = posixpath.join(base_url, relative_path)
            file_path = posixpath.join(url, "index.html")

        if not url.startswith("/"):
            url = "/" + url
        if file_path.startswith("/"):
            file_path = file_path[1:]

        self.file_path = url_safe(file_path)
        self.url = url_safe(url)

    @property
    def posts(self) -> List[Post]:
        start = (self.page - 1) * self.posts_per_page
        end = start + self.posts_per_page
        return self._posts[start:end]

    @property
    def total(self) -> int:
        if self.posts_per_page == 0:
            return 1
        return int((len(self._posts) - 1) / self.posts_per_page) + 1

    @property
    def next(self) -> Optional["Pagination"]:
        if self.page == self.total:
            return None
        return Pagination(
            self._posts,
            self.page + 1,
            self.base_url,
            self.posts_per_page,
        )

    @property
    def prev(self) -> Optional["Pagination"]:
        if self.page == 1:
            return None
        return Pagination(
            self._posts,
            self.page - 1,
            self.base_url,
            self.posts_per_page,
        )

    def iterate(self) -> Iterable["Pagination"]:
        current = self
        for _ in range(self.page - 1, self.total):
            yield current
            current = current.next
            if current is None:
                break

