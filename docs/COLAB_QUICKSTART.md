# COLAB QUICKSTART

Notebook/Colab nên dùng khi máy local yếu hoặc muốn có log train sạch để đưa vào báo cáo.

## 1) Lấy project vào Colab

```python
!git clone https://github.com/imnothoan/doAnChuyenNganh1.git
%cd doAnChuyenNganh1
```

Nếu đang làm từ ZIP local, upload ZIP lên Colab rồi `%cd` vào thư mục gốc.

## 2) Cài dependencies

```python
!python3 -m pip install -r requirements.txt
```

## 3) Train baseline ML

```python
!python3 scripts/download_data.py
!python3 scripts/prepare_data.py
!python3 scripts/train_baseline.py
!python3 scripts/evaluate.py
```

Mặc định pipeline dùng VFND, là dataset đúng nhất cho bài toán fake/real news tiếng Việt trong đồ án. ViFactCheck có thể bật thêm để thí nghiệm fact-checking:

```python
%env INCLUDE_VIFACTCHECK=1
!python3 scripts/download_data.py
```

Không nên bật ViFactCheck cho baseline chính nếu mục tiêu là báo cáo fake-news article, vì phân phối dữ liệu khác VFND.

Kỳ vọng sau khi chạy:

- `models/artifacts/baseline_lr.joblib`
- `models/artifacts/baseline_svm.joblib`
- `models/artifacts/baseline_rf.joblib`
- `models/artifacts/baseline_nb.joblib`
- `models/artifacts/baseline_best.joblib`
- `reports/model_comparison.md`
- `reports/metrics_baseline.json`
- `models/reports/model_metadata.json`

## 4) Xem kết quả nhanh

```python
import json
from pathlib import Path

print(Path("reports/model_comparison.md").read_text())
print(json.dumps(json.loads(Path("models/reports/model_metadata.json").read_text()), indent=2, ensure_ascii=False))
```

## 5) Tải artifacts về máy

```python
from google.colab import files

for path in [
    "models/artifacts/baseline_best.joblib",
    "reports/model_comparison.md",
    "reports/metrics_baseline.json",
    "models/reports/model_metadata.json",
]:
    files.download(path)
```

## 6) Dataset mở rộng

- VFND được tải tự động bằng `scripts/download_data.py`.
- TALLIP repo chỉ chứa metadata; file zip dataset cần tải thủ công theo README của TALLIP rồi giải nén vào `data/raw/tallip/`.
- Kaggle `fakenewvn` có thể thêm thủ công nếu có Kaggle token; đặt CSV vào `data/raw/kaggle_fakenewvn/` rồi chạy lại `prepare/train`.
- ViFactCheck là nguồn mở rộng tùy chọn, bật bằng `INCLUDE_VIFACTCHECK=1`.

## 7) Ghi chú Transformer/PhoBERT

`src/models/train_transformer.py` hiện để chế độ fallback vì fine-tune PhoBERT cần GPU và thêm dependencies nặng. Với Đồ án chuyên ngành 1, baseline TF-IDF + SVM/RF/NB có metrics, confusion matrix, dashboard và feedback loop đã đủ chắc để bảo vệ; PhoBERT nên trình bày là hướng nâng cấp.
