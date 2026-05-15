from __future__ import annotations

import html
import re
import unicodedata


WHITESPACE_PATTERN = re.compile(r"\s+")
URL_PATTERN = re.compile(r"https?://\S+|www\.\S+", flags=re.IGNORECASE)
PUNCTUATION_PATTERN = re.compile(r"[^\w\s]", flags=re.UNICODE)
TOKEN_PATTERN = re.compile(r"\b\w+\b", flags=re.UNICODE)

VIETNAMESE_STOPWORDS = {
    "a",
    "ai",
    "anh",
    "bị",
    "bởi",
    "các",
    "cái",
    "cần",
    "càng",
    "cho",
    "chúng",
    "chưa",
    "chỉ",
    "có",
    "còn",
    "cùng",
    "của",
    "do",
    "đang",
    "đây",
    "đã",
    "đến",
    "để",
    "điều",
    "đó",
    "được",
    "em",
    "gì",
    "hay",
    "hơn",
    "khi",
    "không",
    "là",
    "lại",
    "làm",
    "lên",
    "mà",
    "mình",
    "một",
    "này",
    "nên",
    "nếu",
    "người",
    "như",
    "những",
    "nơi",
    "nữa",
    "ở",
    "phải",
    "qua",
    "ra",
    "rằng",
    "rất",
    "rồi",
    "sau",
    "sẽ",
    "so",
    "sự",
    "tại",
    "theo",
    "thì",
    "trong",
    "trên",
    "từ",
    "và",
    "vào",
    "vẫn",
    "về",
    "vì",
    "việc",
    "với",
}

SUSPICIOUS_TERMS = {
    "clickbait": [
        "sốc",
        "không thể tin",
        "bí mật",
        "kinh hoàng",
        "chấn động",
        "gây sốt",
        "hé lộ",
        "sự thật",
        "bất ngờ",
        "nóng",
    ],
    "emotion": [
        "phẫn nộ",
        "hoang mang",
        "lo sợ",
        "rúng động",
        "đau lòng",
        "cực kỳ",
        "khủng khiếp",
    ],
    "credibility": [
        "chưa kiểm chứng",
        "tin đồn",
        "ẩn danh",
        "không rõ nguồn",
        "lan truyền",
        "nghe nói",
        "theo nguồn tin",
    ],
}


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


def tokenize_vietnamese(text: str, remove_stopwords: bool = True) -> list[str]:
    normalized = basic_clean_text(text).lower()
    normalized = PUNCTUATION_PATTERN.sub(" ", normalized)
    tokens = TOKEN_PATTERN.findall(normalized)
    if remove_stopwords:
        tokens = [token for token in tokens if token not in VIETNAMESE_STOPWORDS and len(token) > 1]
    return tokens


def preprocess_for_ml(text: str) -> str:
    """Normalize text for TF-IDF while keeping Vietnamese accents."""
    return " ".join(tokenize_vietnamese(text, remove_stopwords=True))


def text_statistics(text: str) -> dict[str, int | float]:
    clean = basic_clean_text(text)
    tokens = TOKEN_PATTERN.findall(clean)
    sentences = [item for item in re.split(r"[.!?]+", clean) if item.strip()]
    uppercase = sum(1 for char in clean if char.isupper())
    letters = sum(1 for char in clean if char.isalpha())
    return {
        "characters": len(clean),
        "words": len(tokens),
        "sentences": len(sentences),
        "exclamation_marks": clean.count("!"),
        "question_marks": clean.count("?"),
        "uppercase_ratio": round(uppercase / letters, 4) if letters else 0.0,
    }


def find_suspicious_terms(text: str) -> list[dict[str, str | int]]:
    lowered = basic_clean_text(text).lower()
    findings: list[dict[str, str | int]] = []
    for category, terms in SUSPICIOUS_TERMS.items():
        for term in terms:
            count = lowered.count(term)
            if count:
                findings.append({"term": term, "category": category, "count": count})
    return sorted(findings, key=lambda item: (-int(item["count"]), str(item["term"])))


def highlight_suspicious_terms(text: str) -> str:
    escaped_text = html.escape(basic_clean_text(text))
    terms = sorted(
        {finding["term"] for finding in find_suspicious_terms(text)},
        key=lambda term: len(str(term)),
        reverse=True,
    )
    for term in terms:
        pattern = re.compile(re.escape(str(term)), flags=re.IGNORECASE)
        escaped_text = pattern.sub(
            lambda match: f'<mark class="suspicious-term">{match.group(0)}</mark>',
            escaped_text,
        )
    return escaped_text
