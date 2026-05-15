# Machine Learning-based News Reliability Assessment

Ứng dụng web hỗ trợ đánh giá độ tin cậy của tin tức tiếng Việt bằng NLP/ML. Kiến trúc được tách theo lớp:

- `app/`: Streamlit frontend, nhập text/URL, dashboard kết quả, highlight từ khóa nghi ngờ, lịch sử và feedback.
- `src/features/`: tiền xử lý tiếng Việt, stopword filtering, thống kê văn bản, rule phát hiện clickbait/credibility.
- `src/models/`: train baseline, inference, risk scoring và đóng gói model.
- `src/data/`: tải dataset, chuẩn hóa schema, split train/validation/test, Supabase client.
- `reports/`, `models/`: metrics, confusion matrix, metadata và model artifacts sinh ra sau khi train.

## Quy Ước Nhãn

Dự án dùng quy ước thống nhất:

- `0 = reliable/real`
- `1 = unreliable/fake/clickbait`

Quy ước này khớp với VFND CSV, trong đó `Fake = 1` và `Real = 0`.

## Kết Quả Train Hiện Tại

Pipeline đã train được 4 baseline với TF-IDF:

- Logistic Regression
- Linear SVM
- Random Forest
- Naive Bayes

Trên split hiện tại của VFND đã chuẩn hóa:

- Dataset: `train=350`, `validation=75`, `test=75`
- Best model: `svm`
- Best model sau refit train+validation: Accuracy `0.9200`, F1 macro `0.9199`, ROC-AUC `0.9915`

Chi tiết nằm trong:

- `reports/model_comparison.md`
- `reports/metrics_baseline.json`
- `models/reports/model_metadata.json`

## Chạy Nhanh

```bash
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install -r requirements.txt

python3 scripts/download_data.py
python3 scripts/prepare_data.py
python3 scripts/train_baseline.py
python3 scripts/evaluate.py
streamlit run app/streamlit_app.py
```

Hoặc dùng Makefile:

```bash
make setup
make data
make prepare
make train
make eval
make app
```

## Supabase

Supabase là tùy chọn. Nếu không có `SUPABASE_URL` và `SUPABASE_KEY`, app tự lưu fallback vào:

```text
data/processed/supabase_fallback.jsonl
```

Để dùng Supabase thật, chạy SQL trong `scripts/init_supabase.sql` trên Supabase SQL Editor rồi cấu hình `.env`.
Nếu có PostgreSQL connection string, có thể chạy:

```bash
export SUPABASE_DB_URL="postgresql://..."
make db
```

## Test

```bash
.venv/bin/python -m pytest -q
```

Kết quả hiện tại: `12 passed`.
