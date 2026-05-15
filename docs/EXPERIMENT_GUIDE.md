# EXPERIMENT GUIDE

## Baseline bắt buộc

Các baseline đã được triển khai trong `src/models/train_baseline.py`:

1. TF-IDF + Logistic Regression
2. TF-IDF + Linear SVM
3. TF-IDF + Random Forest
4. TF-IDF + Multinomial Naive Bayes

Best model được chọn theo validation F1 macro, sau đó refit trên `train + validation` và đánh giá lại trên `test`.

## Chỉ số bắt buộc

Pipeline sinh đầy đủ:

- Accuracy
- Precision/Recall/F1 macro
- Precision/Recall/F1 weighted
- ROC-AUC
- Confusion Matrix

File kết quả:

- `reports/metrics_baseline.json`
- `reports/model_comparison.md`
- `reports/figures/confusion_matrix_*.png`
- `models/reports/model_metadata.json`

## Kết quả hiện tại

Dataset sau chuẩn hóa:

- train: 350
- validation: 75
- test: 75
- label 0 reliable/real: 251
- label 1 unreliable/fake/clickbait: 249

Best model hiện tại: `svm`.

Sau refit train+validation, test metrics:

- Accuracy: 0.9200
- F1 macro: 0.9199
- ROC-AUC: 0.9915

## Risk Scoring Trong App

App dùng hai lớp tín hiệu:

- ML probability: xác suất từ model sklearn.
- Lexical risk: điểm phụ từ từ khóa clickbait, cảm xúc, thiếu kiểm chứng, dấu `!`, dấu `?`, uppercase ratio.

`risk_score = max(ML unreliable probability, lexical risk)` để bắt tốt hơn các đoạn text ngắn khi demo.

## Transformer/PhoBERT

`src/models/train_transformer.py` hiện ghi report fallback vì fine-tune PhoBERT cần GPU/Colab và thêm dependencies nặng. Có thể trình bày PhoBERT là hướng nâng cấp sau baseline.

## Reproducibility

- Dùng `RANDOM_STATE` trong `.env`.
- Không commit dữ liệu/model generated vì đã cấu hình trong `.gitignore`.
- Khi chấm/demo, chạy `python3 scripts/evaluate.py` để chứng minh artifacts đầy đủ.
