# Defense Guide

Tài liệu này dùng để chuẩn bị bảo vệ Đồ án chuyên ngành 1 và viết báo cáo.

## 1. Trạng Thái Sẵn Sàng

Dự án đã có đủ các phần bắt buộc cho một đồ án ứng dụng AI/NLP:

- Web app Streamlit chạy được.
- Pipeline tải, chuẩn hóa, split dataset.
- Train thật các mô hình ML baseline.
- Có model artifact để demo ngay.
- Có metrics, confusion matrix, model comparison.
- Có Supabase/PostgreSQL để lưu lịch sử và feedback.
- Có notebook Colab để hội đồng thấy có thể tái lập quá trình train.
- Có unit tests và script kiểm tra artifact.

Không thể cam kết 100% điểm số vì còn phụ thuộc giảng viên, báo cáo PDF, slide và phần trả lời vấn đáp. Tuy vậy, nếu demo ổn và báo cáo trình bày rõ, dự án đã đủ nền tảng để hướng tới mức 9+.

## 2. Demo Flow 7-10 Phút

1. Giới thiệu bài toán:
   - Tin giả/clickbait gây nhiễu thông tin.
   - Mục tiêu là hỗ trợ người dùng đánh giá nhanh độ tin cậy của văn bản/bài báo.

2. Giới thiệu kiến trúc:
   - Frontend: Streamlit.
   - Core Engine: NLP preprocessing, TF-IDF, ML inference, explainability.
   - Database: Supabase/PostgreSQL lưu prediction history và feedback.

3. Mở app:
   - Chọn `Best model`.
   - Dán một đoạn tin chính thống.
   - Bấm phân tích, giải thích các phần: kết luận, risk score, probability chart, token explanation.

4. Dán một đoạn tin nghi ngờ:
   - Ví dụ có các cụm `tin đồn`, `chưa kiểm chứng`, `gây hoang mang`, `sốc`.
   - Chỉ ra highlight từ khóa và lexical risk.

5. Mở tab lịch sử:
   - Chứng minh dữ liệu đã lưu Supabase.
   - Gửi feedback đúng/sai để thể hiện feedback loop.

6. Mở notebook Colab:
   - Chỉ cần cho hội đồng thấy pipeline `download -> prepare -> train -> evaluate`.
   - Không cần train lại trong lúc bảo vệ nếu mất thời gian.

7. Mở reports:
   - `reports/model_comparison.md`
   - `reports/figures/confusion_matrix_svm.png`
   - `models/reports/model_metadata.json`

## 3. Script Thuyết Trình Ngắn

"Em xây dựng công cụ trực quan hóa đánh giá độ tin cậy tin tức tiếng Việt. Hệ thống gồm ba lớp: giao diện Streamlit, lõi xử lý NLP/ML và Supabase/PostgreSQL. Dữ liệu chính là VFND, được chuẩn hóa theo nhãn 0 là tin đáng tin và 1 là tin nghi ngờ. Em huấn luyện bốn mô hình baseline gồm Logistic Regression, Linear SVM, Random Forest và Naive Bayes trên đặc trưng TF-IDF. Mô hình tốt nhất là Linear SVM, đạt Accuracy 0.92 và F1 macro khoảng 0.92 trên tập test sau refit. Ứng dụng không chỉ trả nhãn mà còn hiển thị risk score, biểu đồ xác suất, highlight từ khóa đáng nghi, token explanation và lưu feedback người dùng để phục vụ tái huấn luyện."

## 4. Câu Hỏi Dễ Gặp

**Vì sao dùng TF-IDF + SVM thay vì deep learning?**

Vì đồ án chuyên ngành 1 cần sản phẩm ổn định, giải thích được và train nhanh. Với dataset nhỏ như VFND, TF-IDF + SVM là baseline mạnh, dễ tái lập và phù hợp demo. Deep learning/PhoBERT là hướng nâng cấp khi có nhiều dữ liệu và GPU.

**Risk score có phải xác suất tuyệt đối không?**

Không. Risk score là điểm hỗ trợ quyết định, kết hợp xác suất ML và lexical risk từ các dấu hiệu như từ khóa clickbait, thiếu kiểm chứng, dấu cảm xúc. Nó giúp demo tốt hơn với đoạn văn bản ngắn.

**Dataset có hạn chế gì?**

VFND nhỏ và giai đoạn dữ liệu cũ, nên mô hình chưa thể thay thế fact-checking thật. Dự án định hướng mở rộng bằng TALLIP, Kaggle fakenewvn, ViFactCheck và feedback loop.

**Feedback dùng để làm gì?**

Feedback được lưu vào Supabase. Sau này có thể kiểm duyệt, gán nhãn lại và đưa vào tập retraining để cải thiện model.

**Vì sao cần Supabase?**

Supabase cung cấp PostgreSQL cloud, SDK dễ tích hợp, phù hợp lưu lịch sử phân tích và phản hồi người dùng mà không phải tự vận hành server database.

## 5. Outline Báo Cáo PDF Tối Thiểu 20 Trang

1. Mở đầu: lý do chọn đề tài, mục tiêu, phạm vi.
2. Cơ sở lý thuyết: fake news, NLP, TF-IDF, SVM, Logistic Regression, Random Forest, Naive Bayes.
3. Phân tích yêu cầu: chức năng, phi chức năng, người dùng.
4. Thiết kế hệ thống: layered architecture, use case, data flow.
5. Thiết kế dữ liệu: Supabase schema, prediction history, feedback.
6. Xây dựng dataset: nguồn VFND, cleaning, label convention, split.
7. Xây dựng mô hình: preprocessing, feature extraction, training pipeline.
8. Đánh giá mô hình: metrics, model comparison, confusion matrix.
9. Xây dựng ứng dụng: Streamlit UI, caching, inference, explainability.
10. Kiểm thử: unit tests, pipeline evaluation, demo scenarios.
11. Kết quả đạt được: app, model, database, notebook, reports.
12. Hạn chế và hướng phát triển: mở rộng dataset, PhoBERT, crawler tốt hơn, active learning.
13. Kết luận.
14. Tài liệu tham khảo.

## 6. Outline Slide Tiếng Anh

1. Title and Team Information
2. Problem Statement
3. Objectives and Scope
4. System Architecture
5. Dataset and Label Convention
6. NLP and ML Pipeline
7. Model Comparison
8. Web Application Demo
9. Supabase Feedback Loop
10. Testing and Evaluation
11. Limitations
12. Future Work
13. Conclusion

## 7. Checklist Trước Khi Bảo Vệ

- Chạy `streamlit run app/streamlit_app.py`.
- Kiểm tra `.env` có Supabase URL/key.
- Chạy thử một mẫu reliable và một mẫu unreliable.
- Mở sẵn `reports/model_comparison.md`.
- Mở sẵn confusion matrix.
- Mở sẵn notebook Colab ở trạng thái đã chạy hoặc có output.
- Chuẩn bị câu trả lời về hạn chế dataset và hướng nâng cấp PhoBERT.
