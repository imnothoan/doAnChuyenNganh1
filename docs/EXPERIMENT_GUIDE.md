# EXPERIMENT GUIDE

## Baseline bắt buộc
1. TF-IDF + Logistic Regression
2. TF-IDF + Linear SVM
3. (tùy chọn) Naive Bayes

## Chỉ số bắt buộc
- Accuracy
- Precision/Recall/F1 (macro, weighted)
- Confusion Matrix
- ROC-AUC (nếu khả dụng)

## Transformer (PhoBERT)
- File: `src/models/train_transformer.py`
- Hiện đang để chế độ fallback có hướng dẫn Colab do hạn chế tài nguyên local.

## Reproducibility
- Dùng `RANDOM_STATE` trong `.env`
- Lưu metrics/report theo file trong `reports/`
