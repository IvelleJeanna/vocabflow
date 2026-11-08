#!/usr/bin/env python3
"""Refresh VocabFlow's reading catalogue from public learner/news feeds.

Stores only feed/API metadata and short excerpts, not the full article bodies.
"""
from __future__ import annotations
import html
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

NEWS_BY_LEVELS_API = "https://newsbylevels.com/api/discover.php?" + urllib.parse.urlencode({"limit": 20, "level": 1})
VOA_FEEDS = [
    ("VOA Learning English — Science & Technology", "https://learningenglish.voanews.com/api/zmg_pl-vomx-tpeymtm"),
    ("VOA Learning English — Education", "https://learningenglish.voanews.com/api/ztmp_l-vomx-tpek-__"),
    ("VOA Learning English — Health & Lifestyle", "https://learningenglish.voanews.com/api/zmmpql-vomx-tpey-_q"),
    ("VOA Learning English — Words and Their Stories", "https://learningenglish.voanews.com/api/zmypyl-vomx-tpeyry_"),
]
OUT = Path(__file__).with_name("reading_feed.json")


def http_get(url: str, accept: str) -> bytes:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "VocabFlowPersonalReader/1.0 (static-site feed updater)",
            "Accept": accept,
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        if response.status != 200:
            raise RuntimeError(f"HTTP {response.status} from {url}")
        return response.read()


def clean_excerpt(value: str, limit: int = 360) -> str:
    value = re.sub(r"<[^>]+>", " ", value or "")
    value = html.unescape(re.sub(r"\s+", " ", value)).strip()
    return value[:limit].rstrip()


def read_news_by_levels() -> list[dict]:
    payload = json.loads(http_get(NEWS_BY_LEVELS_API, "application/json").decode("utf-8"))
    items = []
    for article in payload.get("data", []):
        title = str(article.get("title", "")).strip()
        reading_urls = article.get("reading_urls") or {}
        if not title:
            continue
        links = {str(level): str(url) for level, url in reading_urls.items()
                 if str(level) in {"1", "2", "3"} and str(url).startswith("https://")}
        if not links and str(article.get("url", "")).startswith("https://"):
            links = {"1": str(article["url"])}
        if not links:
            continue
        items.append({
            "title": title,
            "topic": str(article.get("topic", "English Reading")),
            "summary": clean_excerpt(str(article.get("summary", ""))),
            "date_published": article.get("date_published"),
            "reading_urls": links,
            "source_name": "News by Levels",
        })
    return items


def read_rss(source_name: str, feed_url: str, limit: int = 6) -> list[dict]:
    root = ET.fromstring(http_get(feed_url, "application/rss+xml, application/xml, text/xml"))
    # VOA feeds are RSS 2.0; namespace fallback keeps the parser tolerant.
    items = root.findall(".//item")
    if not items:
        items = root.findall(".//{*}item")
    output = []
    for item in items[:limit]:
        def field(name: str) -> str:
            node = item.find(name)
            if node is None:
                node = item.find(f"{{*}}{name}")
            return (node.text or "").strip() if node is not None else ""
        title, url = field("title"), field("link")
        if not title or not url.startswith("https://"):
            continue
        raw_date = field("pubDate") or field("date")
        published = None
        if raw_date:
            try:
                published = parsedate_to_datetime(raw_date).astimezone(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
            except (TypeError, ValueError, OverflowError):
                published = raw_date
        output.append({
            "title": title,
            "topic": "VOA Learning English",
            "summary": clean_excerpt(field("description") or field("encoded")),
            "date_published": published,
            "url": url,
            "source_name": source_name,
        })
    return output


def main() -> int:
    all_items: list[dict] = []
    errors: list[str] = []
    try:
        all_items.extend(read_news_by_levels())
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, RuntimeError, KeyError, TypeError) as exc:
        errors.append(f"News by Levels: {exc}")

    for source_name, feed_url in VOA_FEEDS:
        try:
            all_items.extend(read_rss(source_name, feed_url))
        except (urllib.error.URLError, TimeoutError, ET.ParseError, RuntimeError) as exc:
            errors.append(f"{source_name}: {exc}")

    # De-duplicate by canonical article URL while retaining newest source entries.
    unique: dict[str, dict] = {}
    for item in all_items:
        link = next(iter(item.get("reading_urls", {}).values()), item.get("url", ""))
        if link and link not in unique:
            unique[link] = item
    items = list(unique.values())
    items.sort(key=lambda x: str(x.get("date_published") or ""), reverse=True)

    if not items:
        print("No usable stories were returned; keeping the previous feed file. " + " | ".join(errors), file=sys.stderr)
        return 1

    output = {
        "source": "News by Levels public API and VOA Learning English RSS feeds",
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "items": items[:45],
        "warnings": errors,
    }
    tmp = OUT.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(OUT)
    print(f"Updated {OUT.name}: {len(output['items'])} article(s); source warnings: {len(errors)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
