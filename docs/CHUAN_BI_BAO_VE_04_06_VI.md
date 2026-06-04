# File Duy Nhất Chuẩn Bị Bảo Vệ Ngày 04/06/2026

Đề tài: **Machine Learning-based Visual Tool for News Reliability Assessment**

Mục tiêu khi bảo vệ: trình bày dự án như một hệ thống ML/NLP hoàn chỉnh, không phải một app nhập text đơn giản. Thứ tự đúng là: **bài toán -> dataset -> preprocessing -> training -> metrics -> kiến trúc -> demo app -> hạn chế và hướng phát triển**.

Không nói "em chắc chắn model đúng 100%" hoặc "risk score là sự thật tuyệt đối". Câu chuyên nghiệp là:

> "Hệ thống của em là công cụ hỗ trợ sàng lọc ban đầu về độ tin cậy tin tức, không thay thế fact-checking chuyên nghiệp."

## 1. Mở Sẵn Trước Khi Vào Phòng

Mở sẵn các tab/cửa sổ sau:

1. App Streamlit: `http://localhost:8501`
2. Slide PowerPoint em chỉnh: `slides/Major_project_1_slide.pptx`
3. Slide PDF em chỉnh: `slides/Major_project_1_slide.pdf`
4. Lời nói theo slide mới: `slides/SLIDE_SPEAKER_NOTES_VI.md`
5. File ôn kiến thức chi tiết: `docs/ON_TAP_BAO_VE_CHI_TIET_VI.md`
6. File này: `docs/CHUAN_BI_BAO_VE_04_06_VI.md`
7. Report PDF đã format
8. Dataset source VFND: `https://github.com/WhySchools/VFND-vietnamese-fake-news-datasets`
9. Local dataset profile: `reports/dataset_profile.md`
10. Model comparison: `reports/model_comparison.md`
11. Confusion matrix: `reports/figures/confusion_matrix_svm.png`
12. Colab notebook đã train, để sẵn output cũ
13. App tab `History` hoặc Supabase dashboard nếu cần chứng minh lưu dữ liệu

Lệnh chạy app:

```bash
streamlit run app/streamlit_app.py
```

Tuyệt đối không mở `.env`, service role key hoặc database password.

## 2. Có Nên Mở Web Dataset Không?

Có, nên mở sẵn nhưng chỉ dùng trong 20-30 giây. Không tải lại dataset trực tiếp trong buổi bảo vệ.

Tay làm:

1. Mở tab GitHub dataset: `https://github.com/WhySchools/VFND-vietnamese-fake-news-datasets`
2. Chỉ vào tên repo/README: Vietnamese Fake News Dataset.
3. Chỉ nhanh vào phần có cấu trúc nhãn Fake/Real hoặc thư mục CSV.
4. Chuyển ngay sang `reports/dataset_profile.md` để nói dữ liệu em đã xử lý trong project.

Miệng nói:

"Đây là nguồn dataset chính em sử dụng, VFND - Vietnamese Fake News Dataset. Dataset này phục vụ nghiên cứu fake news tiếng Việt và có phân loại Fake/Real. Trong project của em, dữ liệu được chuẩn hóa lại theo quy ước label 0 là reliable/real và label 1 là unreliable/fake/clickbait. Sau bước làm sạch, em tạo các file train, validation và test để huấn luyện mô hình."

Nếu thầy hỏi vì sao không tải ngay trên lớp:

"Dạ dữ liệu đã được tải và tiền xử lý trước để đảm bảo tính tái lập. Trong buổi bảo vệ em chỉ mở nguồn để chứng minh dataset, còn quá trình xử lý được thể hiện ở script và report local."

## 3. Kịch Bản 8-10 Phút

### 0:00 - 0:45: Mở đầu

Nói:

"Kính thưa thầy cô, đề tài của em là Machine Learning-based Visual Tool for News Reliability Assessment. Mục tiêu của đồ án là xây dựng một công cụ web hỗ trợ đánh giá nhanh độ tin cậy của tin tức tiếng Việt bằng xử lý ngôn ngữ tự nhiên và học máy.

Hệ thống không thay thế fact-checking chuyên nghiệp, mà đóng vai trò công cụ hỗ trợ sàng lọc ban đầu. Người dùng có thể nhập nội dung bài viết, xem risk score, xem dấu hiệu ngôn ngữ đáng nghi, xem giải thích từ mô hình, lưu lịch sử và gửi feedback."

### 0:45 - 1:30: Vấn đề và phạm vi

Nói:

"Tin giả và clickbait thường có các dấu hiệu như tiêu đề giật gân, từ ngữ cảm xúc mạnh, thiếu nguồn rõ ràng hoặc kêu gọi chia sẻ. Tuy nhiên, nếu chỉ trả về một nhãn fake/real thì người dùng khó tin tưởng. Vì vậy hệ thống của em tập trung vào cả prediction và explanation: không chỉ dự đoán mà còn giải thích vì sao có rủi ro."

### 1:30 - 2:30: Dataset

Tay làm:

- Mở tab dataset VFND.
- Sau đó mở `reports/dataset_profile.md`.

Nói:

"Nguồn dữ liệu chính là VFND, một dataset fake news tiếng Việt. Em chuẩn hóa nhãn thành 0 là reliable/real và 1 là unreliable/fake/clickbait. Sau bước làm sạch và loại bỏ dữ liệu lỗi, tập processed được chia thành train 350 mẫu, validation 75 mẫu và test 75 mẫu.

Phân bố nhãn sau xử lý khá cân bằng: toàn bộ dữ liệu có khoảng 251 mẫu label 0 và 249 mẫu label 1. Điều này giúp việc đánh giá bằng accuracy và F1 macro có ý nghĩa hơn so với dataset lệch nhãn."

Nếu thầy hỏi dataset nhỏ:

"Dạ dataset còn nhỏ, đây là hạn chế của đồ án. Vì vậy em không tuyên bố hệ thống kiểm chứng sự thật tuyệt đối. Em tập trung xây dựng pipeline ML hoàn chỉnh, có đánh giá định lượng, có explainability và có hướng mở rộng dữ liệu sau này."

### 2:30 - 3:30: Preprocessing và TF-IDF

Nói:

"Pipeline xử lý gồm chuẩn hóa text, loại bỏ dữ liệu lỗi, chuẩn hóa label, tách train/validation/test và trích xuất đặc trưng bằng TF-IDF.

Em chọn TF-IDF vì đây là phương pháp phù hợp với bài toán phân loại văn bản baseline: nhanh, dễ tái lập, hoạt động tốt với dataset nhỏ và giúp giải thích token contribution. Với đồ án chuyên ngành 1, ưu tiên của em là hệ thống chạy ổn định, có thể bảo vệ được về mặt học thuật và giải thích được."

Nếu thầy hỏi stemming/lemmatization:

"Tiếng Việt có đặc thù tách từ phức tạp. Trong phiên bản này em dùng preprocessing cơ bản và TF-IDF để đảm bảo tính ổn định. Hướng phát triển là tích hợp Vietnamese tokenizer hoặc fine-tune PhoBERT khi có dataset lớn hơn."

### 3:30 - 4:45: Training 4 model

Tay làm:

- Mở `reports/model_comparison.md`.

Nói:

"Em không train một model duy nhất. Em huấn luyện và so sánh 4 baseline gồm Logistic Regression, Linear SVM, Random Forest và Multinomial Naive Bayes.

Logistic Regression là baseline tuyến tính dễ hiểu. Linear SVM thường mạnh với dữ liệu TF-IDF thưa và nhiều chiều. Random Forest được dùng để so sánh với hướng tree-based. Naive Bayes là baseline kinh điển cho phân loại văn bản.

Best model được chọn theo validation F1 macro, không chọn cảm tính. Kết quả hiện tại Linear SVM có validation F1 macro cao nhất, nên em chọn Linear SVM làm best model."

Chỉ vào số liệu và nói:

"Sau khi refit, best model đạt Accuracy khoảng 0.92, F1 macro khoảng 0.9199 và ROC-AUC khoảng 0.9915 trên test set."

### 4:45 - 5:45: Kiến trúc hệ thống

Tay làm:

- Mở architecture diagram trong report hoặc app Dashboard.

Nói:

"Hệ thống được thiết kế theo layered architecture. Lớp giao diện dùng Streamlit. Lớp core engine xử lý preprocessing, TF-IDF, inference, risk scoring và explainability. Lớp dữ liệu dùng Supabase/PostgreSQL để lưu prediction history và feedback.

Cách tách lớp này giúp hệ thống dễ bảo trì. Nếu sau này thay SVM bằng PhoBERT, em chỉ cần thay phần core model mà không phải viết lại toàn bộ UI và database workflow."

### 5:45 - 6:45: Dashboard

Tay làm:

- Mở app.
- Chọn `Best model`.
- Bấm tab `Dashboard`.

Nói:

"Đây là dashboard của hệ thống. Dashboard thể hiện bằng chứng triển khai: dataset and training evidence, model benchmark, workflow coverage, benchmark-inspired design và confusion matrix. Điểm em muốn nhấn mạnh là app không chỉ nhập text và trả điểm, mà có workflow từ dữ liệu, mô hình, đánh giá, giải thích, lưu lịch sử và feedback."

Chỉ vào:

- `Best model`
- `Final accuracy`
- `Final F1 macro`
- `Dataset and training evidence`
- `Model benchmark`
- `Workflow coverage`
- `Confusion matrix`

Nếu thầy hỏi từng model, nói ngắn:

- Logistic Regression: "Mô hình tuyến tính, dùng làm baseline dễ hiểu và có xác suất."
- Linear SVM: "Mô hình tuyến tính tối ưu margin, thường mạnh với vector TF-IDF thưa và nhiều chiều; đây là best model của em."
- Random Forest: "Mô hình ensemble cây quyết định, em đưa vào để so sánh với hướng phi tuyến."
- Naive Bayes: "Baseline kinh điển trong phân loại văn bản, train nhanh và phù hợp bag-of-words/TF-IDF."

### 6:45 - 8:00: Demo Case 1 - văn bản đáng tin

Tay làm:

- Copy đoạn dưới đây.
- Vào tab `Analyze`.
- Chọn `Text`.
- Paste vào `Vietnamese news content`.
- Bấm `Analyze`.

Nội dung copy:

```text
Hơn 55 tỷ đồng nâng cấp 8,5 km đại lộ Võ Văn Kiệt ở TP HCM. Dự án sửa chữa, nâng cao độ mặt đường từ cầu Lò Gốm đến giao lộ Ký Con đang được Trung tâm Quản lý đường hầm sông Sài Gòn triển khai. Dự án có tổng mức đầu tư gần 56,5 tỷ đồng, thời gian thi công 240 ngày. Theo đại diện trung tâm, mục tiêu là đảm bảo an toàn giao thông, giảm ngập và cải thiện mỹ quan đô thị.
```

Nói:

"Em bắt đầu với một ca kiểm thử có phong cách tin tức chính thống: có địa điểm, đơn vị triển khai, số liệu đầu tư, thời gian thi công và mục tiêu cụ thể. Sau khi bấm Analyze, hệ thống hiển thị Assessment Summary, Risk score, Confidence, ML risk và Lexical risk.

Ở đây em không chỉ nhìn nhãn reliable/unreliable. Em đọc thêm Why this result để xem rủi ro đến từ ML signal hay lexical signal. Phần token contribution giúp giải thích mô hình thay vì để hệ thống như black box."

### 8:00 - 9:15: Demo Case 2 - văn bản nghi ngờ/clickbait

Tay làm:

- Copy đoạn dưới đây.
- Paste thay văn bản cũ.
- Bấm `Analyze`.

Nội dung copy:

```text
SỐC! Tin đồn chưa kiểm chứng lan truyền trên mạng xã hội cho rằng một sự việc kinh hoàng vừa xảy ra và khiến rất nhiều người hoang mang. Bài viết không nêu nguồn tin chính thức, không có tài liệu xác thực, chỉ kêu gọi mọi người chia sẻ ngay trước khi bị xóa. Nội dung dùng nhiều từ như không thể tin, bí mật, chấn động và gây sốt để thu hút tương tác.
```

Nói:

"Tiếp theo là một ca kiểm thử có nhiều dấu hiệu tin nghi ngờ: từ ngữ cảm xúc mạnh, kêu gọi chia sẻ, không có nguồn chính thức và tự nhận là chưa kiểm chứng. Khi phân tích, hệ thống highlight các từ khóa đáng nghi, lexical risk tăng cao và bảng token contribution cho biết token nào đẩy dự đoán về phía unreliable.

Điều này cho thấy hệ thống không chỉ trả nhãn, mà còn chỉ ra các tín hiệu giúp người dùng hiểu vì sao cần cẩn trọng."

Chỉ vào:

- `Highlighted input`
- `Suspicious signals`
- `Lexical risk`
- `Pushes toward unreliable`

### 9:15 - 9:45: Feedback và History

Tay làm:

- Chọn feedback `Correct`.
- Bấm `Submit feedback`.
- Qua tab `History`.

Nói:

"Sau mỗi lần phân tích, hệ thống lưu prediction history vào Supabase/PostgreSQL. Người dùng có thể gửi feedback đúng, sai hoặc không chắc. Feedback này tạo thành vòng lặp dữ liệu để reviewer kiểm tra lại và dùng cho retraining trong tương lai."

### 9:45 - 10:00: Kết luận

Nói:

"Tóm lại, đồ án của em đã xây dựng được pipeline hoàn chỉnh từ dataset, preprocessing, training, evaluation, inference, visualization, database storage đến feedback loop. Hạn chế hiện tại là dataset còn nhỏ, chưa có evidence retrieval và chưa kiểm chứng claim ở mức sự kiện. Hướng phát triển là mở rộng dataset, fine-tune PhoBERT, thêm source credibility và claim-level evidence retrieval."

## 4. Câu Hỏi Vấn Đáp Quan Trọng

### Có khác gì một ô nhập text rồi trả điểm?

"Khác ở workflow và explainability. Hệ thống có dataset pipeline, benchmark 4 model, metrics thật, risk decomposition, suspicious-term highlighting, token contribution, Supabase history, feedback loop, dashboard và report export."

### Dataset lấy ở đâu?

"Dataset chính là VFND Vietnamese Fake News Dataset trên GitHub. Em mở nguồn dataset để chứng minh, sau đó dữ liệu được xử lý thành các split train/validation/test trong project."

### Label reliable/unreliable có đáng tin không?

"Nhãn dựa trên dataset gốc Fake/Real, sau đó em chuẩn hóa thành 0 reliable/real và 1 unreliable/fake/clickbait. Em thừa nhận chất lượng nhãn phụ thuộc dataset gốc, nên trong báo cáo em trình bày limitation và không khẳng định hệ thống là fact-checker tuyệt đối."

### Vì sao train 4 model?

"Để có benchmark khách quan. Nếu chỉ train một model thì không chứng minh được lựa chọn đó tốt. Em so sánh Logistic Regression, Linear SVM, Random Forest và Naive Bayes, rồi chọn best model theo validation F1 macro."

### Vì sao chọn Linear SVM?

"TF-IDF tạo vector thưa và nhiều chiều. Linear SVM thường mạnh với dạng dữ liệu này vì tìm biên phân tách tốt giữa hai lớp. Trong kết quả thực nghiệm của em, SVM có validation F1 macro cao nhất."

### Risk score có phải xác suất thật không?

"Không hoàn toàn. Risk score là điểm hỗ trợ ra quyết định, kết hợp ML risk và lexical risk. Nó giúp sàng lọc và giải thích rủi ro, nhưng không phải xác suất tuyệt đối của sự thật."

### Vì sao chưa dùng PhoBERT?

"Với dataset nhỏ và yêu cầu demo ổn định, TF-IDF + Linear SVM là baseline mạnh, nhanh, dễ tái lập và dễ giải thích. PhoBERT là hướng phát triển khi có dữ liệu lớn hơn và tài nguyên GPU ổn định."

### Nếu model dự đoán sai thì sao?

"App có feedback form để người dùng đánh dấu đúng/sai/không chắc. Feedback được lưu lại để reviewer kiểm tra và có thể dùng làm dữ liệu retraining sau này."

### Vì sao dùng Supabase?

"Supabase cung cấp PostgreSQL cloud và SDK dễ tích hợp với Streamlit. Trong đồ án này, Supabase dùng để lưu prediction history và feedback, giúp hệ thống có workflow dữ liệu thay vì chỉ chạy cục bộ."

### Vì sao URL mode không phải phần chính?

"URL mode là chức năng hỗ trợ trích xuất nội dung từ allowed domains. Kết quả chính vẫn phải đọc qua explanation. Với fact-check article, bài chính thống có thể chứa từ khóa fake-news vì nó đang nói về một claim giả, nên em không dùng URL label như bằng chứng tuyệt đối."

## 5. Những Câu Không Được Nói

- Không nói: "Em đảm bảo model phát hiện đúng 100% tin giả."
- Không nói: "Risk score là xác suất thật tuyệt đối."
- Không nói: "Dataset lớn và bao phủ mọi loại tin tức."
- Không nói: "URL fact-check này là tin giả."
- Không nói: "Em dùng AI nên kết quả tự động đáng tin."

Nói thay thế:

"Trong phạm vi dataset và task phân loại ngôn ngữ, mô hình đạt kết quả test tốt. Tuy nhiên, fact-checking thật cần thêm evidence retrieval, source verification và claim-level reasoning. Đây là hướng phát triển của hệ thống."

## 6. Checklist 15 Phút Trước Khi Bảo Vệ

- App chạy được tại `http://localhost:8501`.
- Không mở `.env`.
- Mở sẵn VFND GitHub link.
- Mở sẵn `reports/dataset_profile.md`.
- Mở sẵn `reports/model_comparison.md`.
- Mở sẵn `reports/figures/confusion_matrix_svm.png`.
- Test paste Case 1: kết quả dự kiến `Reliable / Low`.
- Test paste Case 2: kết quả dự kiến `Unreliable / High`.
- Test feedback form.
- Mở tab `History`.
- Chuẩn bị câu trả lời về limitation: dataset nhỏ, chưa evidence retrieval, future work PhoBERT.

## 7. Nếu Chỉ Có 5 Phút

Nếu hội đồng cho ít thời gian, rút gọn:

1. 30 giây: giới thiệu bài toán và nói decision-support tool.
2. 45 giây: mở dataset VFND và dataset profile.
3. 60 giây: mở model comparison, nói 4 model và SVM best.
4. 45 giây: mở Dashboard.
5. 90 giây: demo Case 2 nghi ngờ vì trực quan hơn.
6. 30 giây: mở History/feedback.
7. 30 giây: kết luận limitation và future work.

## 8. Câu Kết Thúc Đẹp

"Điểm em tập trung trong đồ án không chỉ là tạo một giao diện dự đoán, mà là xây dựng một workflow ML có thể giải thích và mở rộng: dữ liệu được xử lý có cấu trúc, mô hình được benchmark bằng metrics, kết quả được trực quan hóa, người dùng có thể phản hồi, và hệ thống lưu lại lịch sử để phục vụ cải thiện mô hình trong tương lai."
