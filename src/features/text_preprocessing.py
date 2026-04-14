from __future__ import annotations

import re
import unicodedata


WHITESPACE_PATTERN = re.compile(r"\s+")
URL_PATTERN = re.compile(r"https?://\S+|www\.\S+", flags=re.IGNORECASE)


def normalize_unicode(text: str) -> str:
    return unicodedata.normalize("NFC", text)


def basic_clean_text(text: str) -> str:
    text = normalize_unicode(str(text or ""))
    text = URL_PATTERN.sub(" ", text)
    text = WHITESPACE_PATTERN.sub(" ", text)
    return text.strip()


def combine_title_content(title: str, content: str) -> str:
    title = basic_clean_text(title)
    content = basic_clean_text(content)
    if title and content:
        return f"{title}. {content}".strip()
    return title or content
