# CODELAB TRAINING

## 1. Cài môi trường

```bash
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install -r requirements.txt
cp .env.example .env
```

## 2. Tải dữ liệu

```bash
python3 scripts/download_data.py
```

Nguồn chính:

- VFND: tải tự động từ GitHub.
- TALLIP: repo tải được nhưng data zip có thể cần tải thủ công theo README.
- Kaggle `fakenewvn`: nguồn mở rộng thủ công nếu có Kaggle API token.
- ViFactCheck: nguồn fact-checking mở rộng, chỉ bật khi cần bằng `INCLUDE_VIFACTCHECK=1`.

## 3. Chuẩn hóa dataset

```bash
python3 scripts/prepare_data.py
```

Sinh:

- `data/processed/train.csv`
- `data/processed/val.csv`
- `data/processed/test.csv`
- `reports/dataset_profile.md`

Quy ước nhãn:

- `0 = reliable/real`
- `1 = unreliable/fake/clickbait`

## 4. Train baseline

```bash
python3 scripts/train_baseline.py
```

Model được train:

- `lr`: TF-IDF + Logistic Regression
- `svm`: TF-IDF + Linear SVM
- `rf`: TF-IDF + Random Forest
- `nb`: TF-IDF + Multinomial Naive Bayes

Artifacts:

- `models/artifacts/baseline_lr.joblib`
- `models/artifacts/baseline_svm.joblib`
- `models/artifacts/baseline_rf.joblib`
- `models/artifacts/baseline_nb.joblib`
- `models/artifacts/baseline_best.joblib`
- `models/reports/model_metadata.json`
- `reports/metrics_baseline.json`
- `reports/model_comparison.md`
- `reports/figures/confusion_matrix_*.png`

## 5. Evaluate pipeline outputs

```bash
python3 scripts/evaluate.py
```

Kết quả pass khi `missing_files` rỗng.

## 6. Chạy app

```bash
streamlit run app/streamlit_app.py
```

App có:

- nhập text hoặc URL allowlist;
- cache model bằng `st.cache_resource`;
- risk score kết hợp xác suất ML và lexical risk;
- highlight từ khóa nghi ngờ;
- bảng giải thích token;
- lưu lịch sử và feedback qua Supabase/fallback local.

## 7. Troubleshooting

- `No module named src`: chạy lệnh từ repo root hoặc dùng script trong `scripts/`.
- `python` không tồn tại trên macOS: dùng `python3` hoặc `.venv/bin/python`.
- TALLIP không có CSV sau khi clone: tải zip theo README TALLIP và giải nén vào `data/raw/tallip/`.
- Supabase lỗi key: app tự fallback local vào `data/processed/supabase_fallback.jsonl`.
