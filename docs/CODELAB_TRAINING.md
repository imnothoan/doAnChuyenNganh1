# CODELAB TRAINING

## 1. Cài môi trường
```bash
make setup
cp .env.example .env
```

## 2. Tải dữ liệu
```bash
make data
```
Nếu lỗi tải, làm theo `docs/DATASET_MANUAL.md`.

## 3. Prepare data
```bash
make prepare
```
Sinh các file:
- `data/processed/train.csv`
- `data/processed/val.csv`
- `data/processed/test.csv`
- `reports/dataset_profile.md`

## 4. Train baseline
```bash
make train
```
Sinh artifacts:
- `models/artifacts/baseline_lr.joblib`
- `models/artifacts/baseline_svm.joblib`
- `reports/metrics_baseline.json`
- `reports/model_comparison.md`

## 5. Evaluate pipeline outputs
```bash
make eval
```
Sinh thêm:
- `reports/pipeline_evaluation.json`

## 6. Chạy end-to-end 1 lệnh
```bash
python3 scripts/run_pipeline.py
```
hoặc:
```bash
make all
```

## 7. Chạy local bằng shell script
```bash
./scripts/run_local.sh
```

## Troubleshooting
- **No module named `src`**: chạy từ thư mục root repo hoặc dùng `python3 scripts/<script>.py` (scripts đã bootstrap path tự động).
- **python vs python3**: luôn dùng `python3` hoặc `make` (Makefile đã set `PYTHON ?= python3`).
- **Thiếu `scripts/evaluate.py`**: repo đã bổ sung script này, dùng `make eval` hoặc `python3 scripts/evaluate.py`.
- **Dataset download failed**: xem log trong terminal + `reports/dataset_sources.json`, sau đó làm theo `docs/DATASET_MANUAL.md`.
- **Thiếu dữ liệu**: kiểm tra `data/raw/`.
- **Lỗi package**: chạy lại `make setup`.
