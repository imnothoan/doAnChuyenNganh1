from pathlib import Path

import pandas as pd

from src.data.make_dataset import discover_data_files, read_file_to_dataframe


def test_discover_data_files_supports_csv_json_txt(tmp_path: Path):
    (tmp_path / "a.csv").write_text("title,content,label\nA,B,real\n", encoding="utf-8")
    (tmp_path / "b.json").write_text('[{"title":"A","content":"B","label":"fake"}]', encoding="utf-8")
    (tmp_path / "c.txt").write_text("line 1\nline 2\n", encoding="utf-8")

    files = discover_data_files(tmp_path)
    assert len(files) == 3


def test_read_file_to_dataframe_csv(tmp_path: Path):
    path = tmp_path / "sample.csv"
    path.write_text("title,content,label\nT,C,real\n", encoding="utf-8")

    df = read_file_to_dataframe(path)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 1
