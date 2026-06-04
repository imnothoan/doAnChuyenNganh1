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
export SUPABASE_DB_URL="<connection-string>"
python3 scripts/setup_supabase_db.py
```

Hoặc chạy SQL trong `scripts/init_supabase.sql` trên Supabase SQL Editor.

## Kiểm Thử

```bash
python3 -m pytest -q
```

Kết quả hiện tại: `12 passed`.

## Tài Liệu Báo Cáo Và Bảo Vệ

- `docs/CHUAN_BI_BAO_VE_04_06_VI.md`: file duy nhất nên đọc trước buổi bảo vệ, gồm link dataset, kịch bản nói tiếng Việt, thao tác demo, Q&A và checklist.
- `docs/ON_TAP_BAO_VE_CHI_TIET_VI.md`: tài liệu ôn chi tiết để hiểu dataset, preprocessing, TF-IDF, model, metrics, risk score, explainability và Supabase.
- `slides/Major_project_1_slide.pptx`: slide PowerPoint em đã chỉnh, dùng trực tiếp khi thuyết trình.
- `slides/Major_project_1_slide.pdf`: bản PDF của slide thuyết trình.
- `slides/SLIDE_SPEAKER_NOTES_VI.md`: lời nói tiếng Việt theo đúng 17 slide mới.
- `docs/REPORT_DRAFT.md`: bản nháp báo cáo đầy đủ theo cấu trúc học thuật gồm mở đầu, cơ sở lý thuyết, phân tích thiết kế, triển khai, kết quả và hướng phát triển.
- `docs/DEFENSE_GUIDE.md`: kịch bản demo 7-10 phút, câu hỏi vấn đáp thường gặp, checklist trước khi bảo vệ và outline slide.
- `docs/DEMO_SCRIPT_04_06.md`: kịch bản tay bấm và lời nói chi tiết cho buổi bảo vệ.
- `docs/DEMO_INPUTS_VI.md`: hai case tiếng Việt để copy/paste khi demo thay vì dùng nút sample dựng sẵn.
- `docs/RED_TEAM_AUDIT.md`: tự phản biện theo góc nhìn hội đồng khó tính.
- `docs/PRODUCT_BENCHMARK.md`: so sánh nhanh với các hệ thống fact-checking/news reliability tương tự.
- `reports/figures/report_*.png`: bộ diagram/UML đơn sắc dùng để chèn vào báo cáo.
- `scripts/generate_report_assets.py`: script tái sinh các hình báo cáo.

## Nguồn Dữ Liệu

- VFND: https://github.com/VFND/VFND-vietnamese-fake-news-datasets
- TALLIP FakeNews Dataset: https://github.com/Arko98/TALLIP-FakeNews-Dataset
- ViFactCheck optional extension: https://huggingface.co/datasets/tranthaihoa/vifactcheck
- Kaggle fakenewvn optional extension: https://www.kaggle.com/datasets/chuynvinquc/fakenewvn
