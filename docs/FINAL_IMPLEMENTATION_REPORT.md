# FINAL IMPLEMENTATION REPORT

## Những Gì Đã Hoàn Thiện

- Chuẩn hóa lại toàn bộ quy ước nhãn: `0 = reliable/real`, `1 = unreliable/fake/clickbait`.
- Sửa pipeline đọc VFND để dùng được cả CSV và JSON thô, tự suy luận nhãn từ đường dẫn `Fake/Real/Misleading`.
- Bổ sung preprocessing tiếng Việt cho ML: Unicode NFC, URL cleanup, tokenization, stopword filtering.
- Train đủ 4 mô hình baseline: Logistic Regression, Linear SVM, Random Forest, Naive Bayes.
- Chọn `baseline_best.joblib` theo validation F1 macro và lưu metadata model.
- Bổ sung inference core độc lập với Streamlit, có ML probability, lexical risk và risk score cuối.
- Cải tiến explainability: hỗ trợ mô hình tuyến tính, Naive Bayes và fallback TF-IDF token cho mô hình phi tuyến.
- Nâng Streamlit dashboard: chọn model, cache model, nhập text/URL, risk score, chart, highlight từ khóa nghi ngờ, token explanation, lịch sử và feedback.
- Cập nhật Supabase schema để lưu prediction, probability, risk score, suspicious terms và feedback.
- Cập nhật codelab, Colab quickstart, experiment guide và README.
- Kiểm thử: `12 passed`.

## Kết Quả Train

Dataset sau chuẩn hóa:

- train: 350
- validation: 75
- test: 75
- label 0 reliable/real: 251
- label 1 unreliable/fake/clickbait: 249

Best model: `svm`.

Test metrics sau refit train+validation:

- Accuracy: 0.9200
- F1 macro: 0.9199
- ROC-AUC: 0.9915

## Cách Chạy Demo

```bash
. .venv/bin/activate
python3 scripts/download_data.py
python3 scripts/prepare_data.py
python3 scripts/train_baseline.py
python3 scripts/evaluate.py
streamlit run app/streamlit_app.py
```

## Điểm Nhấn Khi Bảo Vệ

- Có kiến trúc phân lớp rõ: UI, NLP/ML core, data/Supabase.
- Có dataset thật, train thật, metrics thật, confusion matrix thật.
- Có feedback loop để phục vụ tái huấn luyện.
- Có cơ chế caching model trong Streamlit.
- Có fallback local khi chưa cấu hình Supabase.
- Có explainability và highlight từ khóa nghi ngờ để đáp ứng phần trực quan hóa.

## Giới Hạn Cần Nói Rõ

- VFND là dataset nhỏ nên kết quả metrics có thể cao do phạm vi dữ liệu hẹp.
- TALLIP và Kaggle `fakenewvn` nên được dùng để mở rộng nếu cần tăng độ thuyết phục.
- PhoBERT/Transformer chưa fine-tune trong local repo; nên trình bày là hướng nâng cấp trên Colab GPU.
