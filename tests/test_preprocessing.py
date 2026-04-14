from pathlib import Path

import pandas as pd

from src.data.make_dataset import unify_and_clean_dataframe


def test_unify_and_clean_dataframe_removes_duplicates_and_short_texts():
    df = pd.DataFrame(
        {
            "title": ["Tin thật", "Tin giả", "Tin giả", ""],
            "content": [
                "Nội dung đầy đủ cho bản ghi thật.",
                "Nội dung gây nhiễu và sai lệch.",
                "Nội dung gây nhiễu và sai lệch.",
                "ok",
            ],
            "label": ["real", "fake", "fake", "real"],
        }
    )

    cleaned = unify_and_clean_dataframe(df, "vfnd", min_text_length=10)

    assert list(cleaned.columns) == [
        "id",
        "source_dataset",
        "source_type",
        "title",
        "content",
        "text",
        "label",
        "url",
        "published_at",
    ]
    assert len(cleaned) == 2
    assert set(cleaned["label"].tolist()) == {0, 1}


def test_unify_and_clean_dataframe_soft_handles_missing_fields():
    df = pd.DataFrame(
        {
            "headline": ["Tiêu đề"],
            "body": ["Nội dung bài viết tiếng Việt"],
            "class": ["true"],
        }
    )

    cleaned = unify_and_clean_dataframe(df, "custom", min_text_length=5)

    assert cleaned.iloc[0]["title"] == "Tiêu đề"
    assert cleaned.iloc[0]["content"] == "Nội dung bài viết tiếng Việt"
    assert "Tiêu đề" in cleaned.iloc[0]["text"]
    assert cleaned.iloc[0]["label"] == 1


def test_time_split_is_supported_when_published_at_exists(tmp_path: Path):
    df = pd.DataFrame(
        {
            "id": [str(i) for i in range(10)],
            "source_dataset": ["vfnd"] * 10,
            "source_type": ["news"] * 10,
            "title": ["t"] * 10,
            "content": ["đủ dài"] * 10,
            "text": [f"văn bản {i}" for i in range(10)],
            "label": [i % 2 for i in range(10)],
            "url": [""] * 10,
            "published_at": pd.date_range("2024-01-01", periods=10, freq="D").astype(str),
        }
    )

    from src.data.make_dataset import split_dataset

    train_df, val_df, test_df = split_dataset(df, 0.2, 0.2, random_state=42, time_aware=True)

    assert len(train_df) > 0
    assert len(val_df) > 0
    assert len(test_df) > 0
    assert train_df["published_at"].max() <= val_df["published_at"].min()
    assert val_df["published_at"].max() <= test_df["published_at"].min()
