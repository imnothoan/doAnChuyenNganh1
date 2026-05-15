# DATASET SOURCES

## Nguồn Chính

### VFND

- Link: https://github.com/VFND/VFND-vietnamese-fake-news-datasets
- Vai trò: dataset chính cho tiếng Việt, có nhãn Fake/Real.
- Tải tự động: `python3 scripts/download_data.py`
- Ghi chú nhãn: CSV VFND mô tả `Fake = 1`, `Real = 0`, nên toàn dự án dùng `1 = unreliable/fake/clickbait`.

BibTeX theo README VFND:

```tex
@misc{ho_quang_thanh_2019_2578917,
  author       = {Ho Quang Thanh and ninh-pm-se},
  title        = {{thanhhocse96/vfnd-vietnamese-fake-news-datasets:
                   Tập hợp các bài báo tiếng Việt và các bài post
                   Facebook phân loại 2 nhãn Thật \& Giả (228 bài)}},
  month        = feb,
  year         = 2019,
  doi          = {10.5281/zenodo.2578917},
  url          = {https://doi.org/10.5281/zenodo.2578917}
}
```

## Nguồn Mở Rộng

### ViFactCheck

- Link: https://huggingface.co/datasets/tranthaihoa/vifactcheck
- Vai trò: benchmark fact-checking tiếng Việt 7.232 dòng, có claim, context, evidence.
- Tải tùy chọn: `INCLUDE_VIFACTCHECK=1 python3 scripts/download_data.py`
- Ghi chú: không bật mặc định vì đây là fact-checking claim/context, khác phân phối với fake-news article của VFND; dùng làm thí nghiệm mở rộng, không dùng cho baseline chính khi bảo vệ.
- Mapping nhãn trong project:
  - `labels = 0` Supported -> `real/reliable`
  - `labels = 1` Refuted -> `fake/unreliable`
  - `labels = 2` NEI -> `misleading/unreliable`

Citation theo dataset card:

```tex
@inproceedings{tran2025vifactcheck,
  title     = {ViFactCheck: A New Benchmark Dataset and Methods for Multi-Domain News Fact-Checking in Vietnamese},
  author    = {Tran, Thai Hoa and Tran, Quang Duy and Tran, Khanh Quoc and Nguyen, Kiet Van},
  booktitle = {Proceedings of the Thirty-Ninth AAAI Conference on Artificial Intelligence (AAAI-25)},
  pages     = {308--316},
  year      = {2025},
  publisher = {AAAI Press}
}
```

### TALLIP FakeNews Dataset

- Link repo: https://github.com/Arko98/TALLIP-FakeNews-Dataset
- Link paper: https://doi.org/10.1145/3472619
- Vai trò: dataset multilingual có Vietnamese version, phù hợp để mở rộng thí nghiệm.
- Trạng thái: repo tải được nhưng data zip được phân phối qua link trong README; nếu link chậm/timeout thì tải thủ công rồi giải nén vào `data/raw/tallip/`.

### Kaggle Fake News Vietnamese Dataset

- Link: https://www.kaggle.com/datasets/chuynvinquc/fakenewvn
- Vai trò: nguồn mở rộng thủ công nếu có Kaggle token.
- Cách thêm: tải CSV, đặt vào `data/raw/kaggle_fakenewvn/`, chạy lại `prepare/train`.

## Lưu Ý Học Thuật

- Không trộn dataset mà không kiểm tra quy ước nhãn.
- Nếu thêm dataset mới có `1 = real`, cần đảo nhãn trước khi train để giữ thống nhất với project.
- Nên ghi rõ trong báo cáo: kết quả hiện tại dựa chủ yếu trên VFND, dataset nhỏ nên cần mở rộng thêm để đánh giá tổng quát.
