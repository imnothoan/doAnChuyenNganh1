# Hướng Dẫn Bảo Vệ Đồ Án

Tài liệu này là playbook bảo vệ Đồ án chuyên ngành 1 bằng tiếng Việt. App có thể giữ giao diện tiếng Anh để đồng bộ với tên đề tài và báo cáo, nhưng toàn bộ phần em nói với hội đồng nên nói tiếng Việt, rõ ràng và không phóng đại.

## 1. Trạng Thái Sẵn Sàng

Dự án hiện có đủ các phần quan trọng của một đồ án AI/NLP ứng dụng:

- Web app Streamlit chạy được, giao diện tiếng Anh thống nhất.
- Pipeline tải dữ liệu, chuẩn hóa schema, split train/validation/test.
- Huấn luyện thật 4 mô hình baseline: Logistic Regression, Linear SVM, Random Forest, Multinomial Naive Bayes.
- Có best model artifact để demo ngay.
- Có metrics, model comparison, confusion matrix.
- Có Supabase/PostgreSQL để lưu prediction history và feedback.
- Có Colab notebook để tái lập quá trình training.
- Có unit tests và artifact evaluation script.
- Có report draft và UML/report figures.

Không thể cam kết 100% điểm số vì điểm còn phụ thuộc hội đồng, slide, PDF cuối và phần vấn đáp. Tuy vậy, nếu demo đúng kịch bản dưới đây và trả lời rõ hạn chế, dự án đủ nền tảng để hướng tới mức 9+.

## 2. Demo Flow 8-10 Phút

| Thời lượng | Nội dung | Mục tiêu |
|---:|---|---|
| 0:00-0:45 | Giới thiệu bài toán fake news/clickbait | Cho hội đồng hiểu vì sao đề tài có ý nghĩa thực tế |
| 0:45-1:30 | Mục tiêu và phạm vi | Nói rõ đây là decision-support tool, không thay thế fact-checking chuyên nghiệp |
| 1:30-2:30 | Kiến trúc 3 lớp | Streamlit UI, NLP/ML Core, Supabase/PostgreSQL |
| 2:30-3:30 | Dataset và training pipeline | VFND, label convention, TF-IDF, 4 baseline models |
| 3:30-4:30 | Model comparison | Giải thích vì sao chọn Linear SVM |
| 4:30-5:30 | Dashboard hệ thống | Chứng minh có metrics, workflow coverage, confusion matrix |
| 5:30-7:00 | Copy/paste case đáng tin | Cho thấy app phân tích văn bản bình thường và lưu history |
| 7:00-8:30 | Copy/paste case nghi ngờ | Cho thấy risk score, suspicious terms, lexical risk, token explanation |
| 7:30-8:30 | Demo feedback/history | Chứng minh Supabase feedback loop |
| 8:30-9:30 | Mở report/notebook/metrics | Chứng minh sản phẩm có thể tái lập |
| 9:30-10:00 | Kết luận và future work | Nói rõ hạn chế và hướng nâng cấp PhoBERT/evidence retrieval |

## 3. Script Nói Khi Bắt Đầu

"Kính thưa thầy cô, đề tài của em là Machine Learning-based Visual Tool for News Reliability Assessment. Mục tiêu của hệ thống là hỗ trợ người dùng đánh giá nhanh độ tin cậy của một đoạn tin tức tiếng Việt. Hệ thống không thay thế hoàn toàn fact-checking chuyên nghiệp, mà đóng vai trò công cụ hỗ trợ sàng lọc ban đầu bằng NLP và Machine Learning.

Về kiến trúc, em xây dựng theo mô hình phân lớp. Lớp giao diện dùng Streamlit để người dùng nhập văn bản, xem kết quả, xem lịch sử và gửi feedback. Lớp lõi xử lý gồm preprocessing, TF-IDF, model inference, risk scoring và explainability. Lớp dữ liệu dùng Supabase/PostgreSQL để lưu lịch sử dự đoán và phản hồi người dùng.

Về mô hình, em huấn luyện và so sánh 4 baseline gồm Logistic Regression, Linear SVM, Random Forest và Multinomial Naive Bayes. Mô hình tốt nhất được chọn theo validation F1 macro là Linear SVM. Sau khi refit trên train plus validation, model đạt Accuracy khoảng 0.92 và F1 macro khoảng 0.92 trên test set."

## 4. Script Demo App

### 4.1. Case đáng tin

Nói:

"Đầu tiên em copy một ca kiểm thử đã chuẩn bị trong `docs/DEMO_INPUTS_VI.md` và paste vào app như thao tác người dùng thật. Đây là đoạn văn về một dự án hạ tầng giao thông, có đơn vị triển khai, số liệu đầu tư, thời gian thi công và mục tiêu rõ ràng. Sau khi bấm Analyze, hệ thống hiển thị Assessment Summary, Risk score, Confidence, ML risk và Lexical risk.

Ở phần Why this result, app giải thích rõ tín hiệu đến từ mô hình ML hay từ lexical rules. Phần How to read this result giúp người dùng hiểu rằng risk score là điểm hỗ trợ ra quyết định, không phải bằng chứng tuyệt đối."

Điểm cần chỉ vào màn hình:

- Assessment Summary.
- Risk band.
- ML risk vs Lexical risk.
- Highlighted input.
- Model explanation.

### 4.2. Case nghi ngờ/clickbait

Nói:

"Tiếp theo em copy ca kiểm thử thứ hai. Đoạn này có các cụm như tin đồn, chưa kiểm chứng, không rõ nguồn, sốc, chấn động. Khi Analyze, app highlight các từ khóa đáng nghi và lexical risk tăng lên. Điều này giúp hội đồng thấy hệ thống không chỉ trả nhãn, mà còn chỉ ra các dấu hiệu ngôn ngữ."

Điểm cần chỉ vào màn hình:

- Suspicious signals table.
- Highlighted input.
- Lexical risk.
- Token contribution table.

### 4.3. URL mode

Nói:

"URL mode dùng để chứng minh hệ thống có thể trích xuất nội dung từ link bài báo trong allowed domains. Với URL fact-check, cần lưu ý bài báo đó có thể là bài chính thống đang nói về một tin giả, nên model có thể nhận nhiều từ khóa fake-news. Vì vậy em không dùng URL result như bằng chứng tuyệt đối, mà dùng nó để minh họa extraction và explanation."

URL gợi ý:

- Reliable demo: `https://vnexpress.net/sau-cong-nghe-chien-luoc-uu-tien-trien-khai-ngay-5003002.html`
- Fact-check demo: `https://tuoitre.vn/xe-khach-lat-o-deo-phuong-hoang-lam-18-nguoi-chet-la-tin-gia-cau-view-20260526181200255.htm`

## 5. Giải Thích Nhanh Từng Model

| Model | Giải thích ngắn | Vì sao train model này? |
|---|---|---|
| Logistic Regression | A linear probabilistic baseline for sparse text features. | Dễ hiểu, nhanh, có xác suất, làm baseline so sánh. |
| Linear SVM | A margin-based linear classifier that works well with high-dimensional TF-IDF vectors. | Thường mạnh trong text classification và là best model của dự án. |
| Random Forest | An ensemble of decision trees used as a non-linear comparison model. | Cho thấy em có thử hướng tree-based, không chỉ thử linear model. |
| Multinomial Naive Bayes | A fast probabilistic classifier commonly used for bag-of-words or TF-IDF text. | Baseline kinh điển trong phân loại văn bản, train rất nhanh. |
| Best model | Linear SVM selected by validation F1 macro. | Chọn dựa trên metric, không chọn cảm tính. |

## 6. Câu Hỏi Vấn Đáp Dễ Gặp

**Vì sao train 4 model mà app chỉ dùng Best model?**

Em train nhiều model để so sánh khách quan. Sau đó em chọn model tốt nhất theo validation F1 macro và export thành `baseline_best.joblib` để app dùng ổn định khi demo.

**Vì sao Linear SVM tốt nhất?**

TF-IDF tạo vector rất thưa và nhiều chiều. Linear SVM thường hoạt động tốt trong không gian như vậy vì nó tìm ranh giới tuyến tính có margin lớn giữa hai lớp. Trong kết quả của em, SVM có validation F1 macro cao nhất nên được chọn.

**Logistic Regression khác SVM thế nào?**

Logistic Regression tối ưu xác suất phân loại, còn Linear SVM tối ưu biên phân tách giữa hai lớp. Cả hai đều là linear model, nhưng mục tiêu tối ưu khác nhau.

**Random Forest dùng cho text có hợp không?**

Random Forest không phải lựa chọn mạnh nhất cho TF-IDF sparse features, nhưng em đưa vào để so sánh với một mô hình phi tuyến/tree-based. Kết quả cho thấy nó không vượt SVM trong bài toán này.

**Naive Bayes có giả định gì?**

Naive Bayes giả định các đặc trưng độc lập có điều kiện theo nhãn. Giả định này đơn giản nhưng thường vẫn hiệu quả trong phân loại văn bản.

**Risk score có phải xác suất thật không?**

Không hoàn toàn. Risk score là decision-support score. Nó kết hợp ML risk và lexical risk bằng cách lấy tín hiệu rủi ro mạnh hơn. Vì vậy nó giúp sàng lọc và giải thích, nhưng không phải xác suất sự thật tuyệt đối.

**Vì sao chưa dùng PhoBERT hoặc deep learning?**

Đồ án chuyên ngành 1 cần sản phẩm ổn định, dễ demo, dễ giải thích và tái lập. Với dataset nhỏ, TF-IDF + SVM là baseline mạnh, nhanh và explainable. PhoBERT là hướng phát triển khi có nhiều dữ liệu hơn và GPU ổn định.

**Dataset có hạn chế gì?**

VFND nhỏ và không bao phủ toàn bộ tin tức hiện đại. Vì vậy em trình bày hệ thống là công cụ hỗ trợ đánh giá độ tin cậy dựa trên dấu hiệu ngôn ngữ, không phải công cụ kiểm chứng sự thật tuyệt đối.

**Vì sao cần Supabase?**

Supabase cung cấp PostgreSQL cloud và SDK dễ tích hợp. Trong đồ án, Supabase dùng để lưu prediction history và feedback, tạo feedback loop cho retraining sau này.

**Nếu model dự đoán sai thì sao?**

App có feedback form để người dùng đánh dấu đúng/sai/không chắc. Các feedback này có thể được review, làm sạch và đưa vào tập retraining ở phiên bản sau.

## 7. Outline Slide Gợi Ý

1. Tên đề tài và thông tin nhóm
2. Vấn đề cần giải quyết
3. Mục tiêu và phạm vi hệ thống
4. Khảo sát hệ thống tương tự
5. Kiến trúc phân lớp
6. Dataset và quy ước nhãn
7. NLP/ML pipeline
8. So sánh mô hình
9. Best model: TF-IDF + Linear SVM
10. Demo ứng dụng web
11. Explainability và risk score
12. Supabase feedback loop
13. Kiểm thử và đánh giá
14. Hạn chế và hướng phát triển

## 8. Checklist Trước Khi Bảo Vệ

- Chạy app: `streamlit run app/streamlit_app.py`.
- Mở sẵn app tại `http://localhost:8501`.
- Chọn `Best model`.
- Mở sẵn `docs/DEMO_INPUTS_VI.md` hoặc Google Docs chứa hai case demo.
- Test copy/paste case đáng tin.
- Test copy/paste case nghi ngờ.
- Test feedback form.
- Mở History tab để chứng minh dữ liệu đã lưu.
- Mở `reports/model_comparison.md`.
- Mở `reports/figures/confusion_matrix_svm.png`.
- Mở `notebooks/colab_train_baseline.ipynb`.
- Mở report PDF đã format.
- Chuẩn bị câu trả lời về limitation: dataset nhỏ, không thay thế fact-checking, future work là PhoBERT/evidence retrieval.

## 9. Điều Không Nên Nói Khi Bảo Vệ

- Không nói "model phát hiện đúng 100% tin giả".
- Không nói "risk score là xác suất thật tuyệt đối".
- Không nói "URL fact-check là tin giả". Hãy nói đó là bài chính thống nói về một claim giả.
- Không train lại model trực tiếp trong buổi bảo vệ nếu không cần thiết.
- Không mở file `.env` hoặc bất kỳ secret key nào trước hội đồng.
