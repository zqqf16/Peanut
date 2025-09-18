"""Integration helpers for Ghost admin API."""

from __future__ import annotations

import logging
from typing import Iterable, Optional
from urllib.parse import urljoin

import requests

logging.getLogger("requests").setLevel(logging.CRITICAL)
SESSION = requests.Session()


def api_path(url: str, path: str) -> str:
    base = url.rstrip("/") + "/ghost/api/v0.1/"
    return urljoin(base, path.lstrip("/"))


def get_token(url: str, user: str, password: str) -> Optional[str]:
    if not url or not user or not password:
        logging.error("Invalid url/username/password")
        return None

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = (
        "grant_type=password"
        f"&username={user}"
        f"&password={password}"
        "&client_id=ghost-admin"
        "&client_secret=8b4a248000cd"
    )

    response = SESSION.post(api_path(url, "authentication/token"), data=data, headers=headers)
    if response.status_code != 200:
        logging.error("Failed to get token, please check your username or password")
        return None

    return response.json().get("access_token")


def post_to_json(post) -> dict:
    date = post.date.strftime("%Y-%m-%dT%H:%M:%SZ")
    return {
        "status": "published" if post.publish else "draft",
        "title": post.title,
        "slug": post.slug,
        "markdown": post.raw,
        "image": post.image,
        "page": post.top,
        "language": "zh_CN",
        "meta_title": None,
        "meta_description": None,
        "author": 1,
        "created_at": date,
        "created_by": 1,
        "published_at": date,
        "published_by": 1,
    }


def push(url: str, token: str, posts: Iterable) -> None:
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    endpoint = api_path(url, "posts/")
    for post in posts:
        logging.info("Pushing %s", post.title, prefix="   ↳  ")
        payload = {"posts": [post_to_json(post)]}
        response = SESSION.post(endpoint, headers=headers, json=payload)
        if response.status_code != 201:
            logging.error(
                "Push post failed, status code: %s, %s",
                response.status_code,
                response.text,
            )

