# COLAB QUICKSTART

## 1) Lấy project vào Colab
```python
!git clone https://github.com/imnothoan/doAnChuyenNganh1.git
%cd doAnChuyenNganh1
```

Hoặc upload ZIP project rồi `cd` vào thư mục gốc.

## 2) Cài dependencies
```python
!python3 -m pip install -r requirements.txt
```

## 3) Chạy baseline pipeline
```python
!python3 scripts/download_data.py
!python3 scripts/prepare_data.py
!python3 scripts/train_baseline.py
!python3 scripts/evaluate.py
```

## 4) Tải artifacts về máy
```python
from google.colab import files
files.download("models/artifacts/baseline_lr.joblib")
files.download("models/artifacts/baseline_svm.joblib")
files.download("reports/metrics_baseline.json")
```

## Ghi chú Transformer
- Nếu local không đủ tài nguyên để train transformer, ưu tiên chạy `scripts/train_transformer.py` trên Colab GPU.
