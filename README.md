# News Reliability Assessment

Ứng dụng web đánh giá độ tin cậy của tin tức tiếng Việt bằng NLP và Machine Learning.

## Mục Tiêu

- Phân loại nội dung tin tức thành `reliable/real` hoặc `unreliable/fake/clickbait`.
- Trực quan hóa kết quả dự đoán bằng risk score, biểu đồ xác suất, highlight từ khóa nghi ngờ và giải thích token.
- Lưu lịch sử phân tích và feedback người dùng vào Supabase/PostgreSQL để phục vụ tái huấn luyện.

## Kiến Trúc

```text
app/                 Streamlit UI
src/data/            Dataset pipeline + Supabase client
src/features/        NLP preprocessing + suspicious keyword rules
src/models/          Training, inference, risk scoring
src/explainability/  Token-level explanation
src/evaluation/      Artifact verification
scripts/             CLI pipeline scripts
notebooks/           Colab training notebook
models/              Best trained model + metadata
reports/             Metrics, dataset profile, confusion matrices
tests/               Unit tests
```

## Quy Ước Nhãn

- `0 = reliable/real`
- `1 = unreliable/fake/clickbait`

Quy ước này khớp VFND, trong đó `Fake = 1` và `Real = 0`.

## Kết Quả Hiện Tại

Dataset chính: VFND Vietnamese Fake News Dataset.

- Train: `350`
- Validation: `75`
- Test: `75`
- Best model: `TF-IDF + Linear SVM`
- Accuracy: `0.9200`
- F1 macro: `0.9199`
- ROC-AUC: `0.9915`

Artifacts quan trọng:

- `models/artifacts/baseline_best.joblib`
- `models/reports/model_metadata.json`
- `reports/model_comparison.md`
- `reports/metrics_baseline.json`
- `reports/figures/confusion_matrix_svm.png`

## Chạy Ứng Dụng

```bash
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install -r requirements.txt
streamlit run app/streamlit_app.py
```

## Train Lại Model

```bash
python3 scripts/download_data.py
python3 scripts/prepare_data.py
python3 scripts/train_baseline.py
python3 scripts/evaluate.py
```

Hoặc chạy toàn bộ pipeline:

```bash
python3 scripts/run_pipeline.py
```

Notebook Colab:

- `notebooks/colab_train_baseline.ipynb`

## Supabase

Copy `.env.example` thành `.env`, điền:

```text
SUPABASE_URL=https://<project-ref>.supabase.co
SUPABASE_KEY=<anon-or-publishable-key>
```

Khởi tạo schema:

```bash
export SUPABASE_DB_URL="postgresql://..."
python3 scripts/setup_supabase_db.py
```

Hoặc chạy SQL trong `scripts/init_supabase.sql` trên Supabase SQL Editor.

## Kiểm Thử

```bash
python3 -m pytest -q
```

Kết quả hiện tại: `12 passed`.

## Nguồn Dữ Liệu

- VFND: https://github.com/VFND/VFND-vietnamese-fake-news-datasets
- TALLIP FakeNews Dataset: https://github.com/Arko98/TALLIP-FakeNews-Dataset
- ViFactCheck optional extension: https://huggingface.co/datasets/tranthaihoa/vifactcheck
- Kaggle fakenewvn optional extension: https://www.kaggle.com/datasets/chuynvinquc/fakenewvn
