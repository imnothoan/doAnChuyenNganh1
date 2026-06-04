# Kịch Bản Bảo Vệ Ngày 04/06/2026

Tài liệu này viết bằng tiếng Việt để em dùng trực tiếp khi bảo vệ. Mục tiêu là trình bày như một đồ án chuyên ngành có ML thật: bắt đầu từ bài toán, dữ liệu, pipeline huấn luyện, đánh giá định lượng, rồi mới demo ứng dụng.

Không hứa hệ thống đúng 100%. Câu an toàn và chuyên nghiệp là: "Hệ thống là công cụ hỗ trợ sàng lọc ban đầu, không thay thế fact-checking chuyên nghiệp."

## 0. Chuẩn Bị Trước Khi Vào Phòng

Mở sẵn các cửa sổ sau:

1. App Streamlit: `http://localhost:8501`
2. File nội dung demo: `docs/DEMO_INPUTS_VI.md`
3. Report PDF đã format
4. `reports/dataset_profile.md`
5. `reports/model_comparison.md`
6. `reports/figures/confusion_matrix_svm.png`
7. Notebook Colab đã train, để sẵn output cũ
8. Supabase dashboard hoặc tab `History` trong app

Lệnh chạy app:

```bash
streamlit run app/streamlit_app.py
```

Tuyệt đối không mở `.env`, service role key hoặc database password trước hội đồng.

## 1. Mở Đầu - 45 Giây

Nói:

"Kính thưa thầy cô, đề tài của em là Machine Learning-based Visual Tool for News Reliability Assessment. Mục tiêu của đồ án là xây dựng một công cụ web hỗ trợ đánh giá nhanh độ tin cậy của tin tức tiếng Việt bằng xử lý ngôn ngữ tự nhiên và học máy.

Em xin nhấn mạnh hệ thống không thay thế fact-checking chuyên nghiệp. Hệ thống đóng vai trò decision-support tool, tức là hỗ trợ sàng lọc ban đầu, hiển thị risk score, dấu hiệu ngôn ngữ đáng nghi, giải thích từ mô hình và lưu phản hồi người dùng để cải thiện về sau."

Tay làm:

- Mở slide/report title.
- Chưa mở app ngay.

## 2. Nói Về Dataset - 60 Giây

Tay làm:

- Mở `reports/dataset_profile.md`.

Nói:

"Về dữ liệu, em sử dụng dataset tiếng Việt phục vụ bài toán fake news/reliability assessment. Sau bước làm sạch, dataset được chia thành train, validation và test. Cụ thể train có 350 mẫu, validation có 75 mẫu và test có 75 mẫu.

Nhãn được chuẩn hóa theo quy ước: label 0 là reliable hoặc real news, label 1 là unreliable, fake hoặc clickbait. Trong toàn bộ dữ liệu sau xử lý, phân bố nhãn khá cân bằng, khoảng 251 mẫu label 0 và 249 mẫu label 1. Em cũng loại bỏ dữ liệu lỗi như thiếu nhãn, văn bản quá ngắn và duplicate."

Nếu thầy hỏi dữ liệu có nhỏ không:

"Dạ dataset còn nhỏ, đây là hạn chế em có ghi trong báo cáo. Vì vậy em chọn baseline model dễ tái lập, có đánh giá định lượng và có explainability, thay vì khẳng định hệ thống có thể kiểm chứng sự thật tuyệt đối."

## 3. Nói Về Preprocessing Và Feature Extraction - 60 Giây

Tay làm:

- Chỉ vào pipeline diagram hoặc phần ML pipeline trong report.

Nói:

"Sau khi có dữ liệu, em xây dựng pipeline xử lý gồm các bước: chuẩn hóa text, loại bỏ bản ghi lỗi, chuẩn hóa label, tách train/validation/test, sau đó trích xuất đặc trưng bằng TF-IDF.

TF-IDF phù hợp với đồ án này vì văn bản tin tức có nhiều từ/cụm từ mang tín hiệu phân loại, ví dụ những cụm từ có tính giật gân, chưa kiểm chứng hoặc thiếu nguồn rõ ràng. TF-IDF cũng giúp mô hình tuyến tính dễ giải thích hơn thông qua token contribution."

Nếu thầy hỏi vì sao không stemming/lemmatization sâu:

"Tiếng Việt có đặc thù tách từ và ngữ cảnh phức tạp. Trong phạm vi đồ án này, em ưu tiên pipeline ổn định, tái lập được và giải thích được. Hướng phát triển sau là dùng tokenizer tiếng Việt tốt hơn hoặc fine-tune PhoBERT."

## 4. Nói Về Training 4 Model - 75 Giây

Tay làm:

- Mở `reports/model_comparison.md`.

Nói:

"Em không chỉ train một model duy nhất. Em huấn luyện và so sánh 4 baseline: Logistic Regression, Linear SVM, Random Forest và Multinomial Naive Bayes.

Logistic Regression là baseline tuyến tính có xác suất, dễ hiểu. Linear SVM phù hợp với dữ liệu TF-IDF thưa và nhiều chiều. Random Forest được dùng như mô hình tree-based để so sánh hướng phi tuyến. Naive Bayes là baseline kinh điển trong phân loại văn bản.

Em chọn best model dựa trên validation F1 macro, không chọn theo cảm tính. Trong kết quả hiện tại, Linear SVM có validation F1 macro cao nhất nên được chọn làm best model."

Chỉ vào số liệu:

"Sau khi refit, best model đạt Accuracy khoảng 0.92, F1 macro khoảng 0.9199 và ROC-AUC khoảng 0.9915 trên test set."

## 5. Nói Về Kiến Trúc Hệ Thống - 60 Giây

Tay làm:

- Mở architecture diagram trong report hoặc dashboard app.

Nói:

"Hệ thống được thiết kế theo layered architecture. Lớp giao diện dùng Streamlit để nhập văn bản, xem biểu đồ, xem giải thích và gửi feedback. Lớp core engine gồm preprocessing, TF-IDF, model inference, risk scoring và explainability. Lớp dữ liệu dùng Supabase/PostgreSQL để lưu lịch sử phân tích và phản hồi.

Cách tách lớp này giúp hệ thống dễ bảo trì. Nếu sau này thay Linear SVM bằng PhoBERT, em chỉ cần thay phần core model mà không phải viết lại toàn bộ giao diện và database workflow."

## 6. Mở App Và Dashboard - 75 Giây

Tay làm:

- Mở app.
- Chọn `Best model`.
- Bấm tab `Dashboard`.

Nói:

"Đây là dashboard của hệ thống. Phần này thể hiện bằng chứng triển khai chứ không chỉ là giao diện nhập text. Dashboard có dataset and training evidence, model benchmark, workflow coverage, benchmark-inspired design và confusion matrix.

Điểm em muốn nhấn mạnh là hệ thống có đủ workflow: nhập bài viết, chạy NLP/ML inference, hiển thị risk score, giải thích kết quả, lưu history, nhận feedback và xuất case report."

Chỉ nhanh vào:

- `Best model`
- `Final accuracy`
- `Final F1 macro`
- `Dataset and training evidence`
- `Model benchmark`
- `Workflow coverage`
- `Confusion matrix`

## 7. Demo Case Đáng Tin - 90 Giây

Tay làm:

- Mở `docs/DEMO_INPUTS_VI.md` hoặc Google Docs đã copy sẵn.
- Copy Case 1.
- Qua app tab `Analyze`.
- Chọn `Text`.
- Paste vào `Vietnamese news content`.
- Bấm `Analyze`.

Nói:

"Em bắt đầu với một ca kiểm thử có phong cách tin tức chính thống. Văn bản có địa điểm, đơn vị triển khai, số liệu đầu tư, thời gian thi công và mục tiêu cụ thể.

Sau khi bấm Analyze, hệ thống hiển thị Assessment Summary, Risk score, Confidence, ML risk và Lexical risk. Ở đây em không chỉ nhìn nhãn reliable/unreliable, mà đọc thêm phần Why this result để biết tín hiệu chính đến từ mô hình ML hay từ lexical rules."

Chỉ vào:

- `Assessment Summary`
- `Risk score`
- `ML risk`
- `Lexical risk`
- `Why this result?`
- `Model explanation`

Nói thêm:

"Phần token contribution giúp em giải thích mô hình thay vì chỉ đưa ra một con số. Đây là điểm quan trọng để tránh việc hệ thống bị xem như black box."

## 8. Demo Case Nghi Ngờ/Clickbait - 90 Giây

Tay làm:

- Copy Case 2 trong `docs/DEMO_INPUTS_VI.md`.
- Paste thay văn bản cũ.
- Bấm `Analyze`.

Nói:

"Tiếp theo em dùng một ca kiểm thử có nhiều dấu hiệu tin nghi ngờ: từ ngữ cảm xúc mạnh, kêu gọi chia sẻ, không nêu nguồn chính thức và tự nhận là chưa kiểm chứng.

Khi phân tích, hệ thống highlight các từ khóa đáng nghi, lexical risk tăng cao và bảng token contribution cho biết token nào đẩy dự đoán về phía unreliable. Điều này giúp người dùng không chỉ nhận nhãn, mà còn hiểu vì sao hệ thống cảnh báo."

Chỉ vào:

- `Highlighted input`
- `Suspicious signals`
- `Lexical risk`
- `Pushes toward unreliable`

## 9. Demo Feedback, History Và Report Export - 60 Giây

Tay làm:

- Ở dưới kết quả, chọn feedback `Correct`.
- Bấm `Submit feedback`.
- Bấm `Download analysis report` nếu muốn.
- Qua tab `History`.

Nói:

"Sau mỗi lần phân tích, hệ thống lưu prediction history vào Supabase/PostgreSQL. Người dùng có thể gửi feedback đúng, sai hoặc không chắc. Feedback này tạo thành vòng lặp cải thiện dữ liệu cho lần retraining sau.

Ngoài ra, app có thể xuất analysis report cho từng ca. Điều này biến hệ thống từ một trang trả điểm đơn giản thành workflow hỗ trợ reviewer."

## 10. URL Mode - Chỉ Demo Nếu Còn Thời Gian

Tay làm:

- Chọn `URL`.
- Paste URL tin đáng tin hoặc fact-check URL.

Nói:

"URL mode dùng để chứng minh hệ thống có khả năng trích xuất nội dung từ bài báo thuộc allowed domains. Với bài fact-check, cần lưu ý rằng đó có thể là bài chính thống đang nói về một claim giả, nên nội dung vẫn chứa nhiều từ khóa fake-news. Vì vậy em luôn đọc kết quả cùng explanation, không xem label là chân lý tuyệt đối."

## 11. Kết Luận - 30 Giây

Nói:

"Tóm lại, đồ án của em đã xây dựng được một pipeline hoàn chỉnh từ dataset, preprocessing, training, evaluation, inference, visualization, database storage đến feedback loop. Hệ thống hiện tại phù hợp vai trò hỗ trợ sàng lọc độ tin cậy tin tức tiếng Việt.

Hạn chế là dataset còn nhỏ, chưa có evidence retrieval và chưa kiểm chứng claim ở mức sự kiện. Hướng phát triển là mở rộng dataset, fine-tune PhoBERT, thêm source credibility và claim-level evidence retrieval."

## 12. Câu Trả Lời Khẩn Cấp Khi Bị Hỏi Vặn

**Có khác gì một ô nhập text rồi trả điểm?**

"Khác ở workflow và explainability. Hệ thống có dataset pipeline, benchmark 4 model, metrics thật, risk decomposition, suspicious-term highlighting, token contribution, Supabase history, feedback loop, dashboard và report export."

**Kết quả có đáng tin không?**

"Đáng tin trong phạm vi dataset và task phân loại ngôn ngữ, vì em có test metrics và confusion matrix. Nhưng em không nói nó kiểm chứng sự thật tuyệt đối. Fact-checking thật cần thêm evidence retrieval và source verification."

**Vì sao không dùng deep learning/PhoBERT?**

"Với dataset nhỏ và yêu cầu demo ổn định, TF-IDF + Linear SVM là baseline mạnh, nhanh, dễ tái lập và giải thích được. PhoBERT là hướng phát triển khi có thêm dữ liệu và GPU."

**Nếu model dự đoán sai thì sao?**

"App có feedback form để người dùng đánh dấu đúng/sai/không chắc. Dữ liệu feedback được lưu lại để reviewer kiểm tra và dùng làm nguồn retraining sau này."

**Dataset nhỏ thì có đủ không?**

"Dataset nhỏ là hạn chế, nhưng em xử lý bằng cách tách train/validation/test, so sánh nhiều baseline, báo cáo metrics rõ ràng và không tuyên bố quá mức. Trọng tâm đồ án là xây dựng pipeline ML ứng dụng hoàn chỉnh và có khả năng mở rộng."
