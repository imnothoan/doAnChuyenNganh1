# FINAL IMPLEMENTATION REPORT

## Những gì đã làm
- Thiết kế lại cấu trúc dự án theo chuẩn dữ liệu/model/reports/src/scripts/docs/tests.
- Xây pipeline tải dataset với metadata và fallback tài liệu thủ công.
- Xây pipeline preprocessing tiếng Việt, chuẩn hóa schema, label binary, split train/val/test.
- Huấn luyện baseline LR/SVM/(NB) và xuất artifacts + metrics + confusion matrix + model comparison.
- Tạo module explainability cho mô hình tuyến tính.
- Tạo Streamlit MVP có nhập text/URL, dự đoán, giải thích, lưu lịch sử.
- Tạo Supabase client dạng fallback-safe bằng biến môi trường.
- Tạo codelab tài liệu và Makefile tự động hóa.
- Tạo test cơ bản cho preprocessing và định dạng output inference.

## Cách chạy nhanh
```bash
make setup
make data
make prepare
make train
make app
```

## Giới hạn hiện tại
- Transformer/PhoBERT đang là stub fallback, chưa fine-tune full local.
- Chất lượng phụ thuộc dữ liệu đầu vào thực tế và độ sạch nguồn.
- URL extraction hiện mức cơ bản (HTML paragraph).

## Kế hoạch nâng cấp
- Fine-tune PhoBERT đầy đủ trên Colab/GPU.
- Tích hợp active learning từ feedback người dùng.
- Thêm drift monitoring theo thời gian và cảnh báo suy giảm chất lượng.
