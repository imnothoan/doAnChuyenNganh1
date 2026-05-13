# Vietnamese News Reliability Evaluation (NLP/ML)

Dự án xây dựng pipeline đánh giá độ tin cậy tin tức tiếng Việt: tải dữ liệu, chuẩn hóa, huấn luyện baseline, giải thích kết quả và chạy Streamlit MVP.

## Cấu trúc chính
- `data/`: raw/interim/processed
- `src/`: code pipeline
- `scripts/`: lệnh chạy nhanh
- `app/`: Streamlit
- `docs/`: codelab và tài liệu vận hành
- `tests/`: test cơ bản

## Chạy nhanh
```bash
make setup
make all
make app
```

Hoặc chạy pipeline tuần tự bằng Python:
```bash
python3 scripts/run_pipeline.py
```

## Test
```bash
python -m pytest -q
```

## Ghi chú
- Toàn bộ đọc/ghi text dùng UTF-8.
- Không hardcode key: dùng `.env` theo mẫu `.env.example`.
- Nếu không tải được dataset tự động, xem `docs/DATASET_MANUAL.md`.
