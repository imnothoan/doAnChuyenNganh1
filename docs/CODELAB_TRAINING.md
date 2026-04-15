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

## 5. Evaluate/Explain
```bash
make eval
```

## Troubleshooting
- Thiếu dữ liệu: kiểm tra `data/raw/`
- Lỗi encoding: đảm bảo UTF-8
- Lỗi package: chạy lại `make setup`
