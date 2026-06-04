# Lời Nói Theo Slide Mới Của Em

File slide chính:

- `slides/Major_project_1_slide.pptx`
- `slides/Major_project_1_slide.pdf`

File này khớp với **17 slide** trong bản PDF/PPTX em đã tự chỉnh. Khi thuyết trình, em không cần đọc y nguyên; hãy dùng như khung nói. Mục tiêu là nói tự nhiên, chắc kiến thức, không bị rơi vào kiểu đọc slide.

## Slide 1 - Title

Nói:

"Kính thưa thầy cô, đề tài của em là Machine Learning-based Visual Tool for News Reliability Assessment. Mục tiêu của đồ án là xây dựng một công cụ web hỗ trợ đánh giá nhanh độ tin cậy của tin tức tiếng Việt bằng NLP và Machine Learning.

Hệ thống cho phép người dùng nhập nội dung tin tức, sau đó trả về nhãn đánh giá, risk score, các tín hiệu ngôn ngữ đáng nghi, phần giải thích và lịch sử phân tích."

Chốt ý:

"Em xin nhấn mạnh hệ thống đóng vai trò hỗ trợ sàng lọc ban đầu, không thay thế fact-checking chuyên nghiệp."

## Slide 2 - Table of Contents

Nói:

"Bài trình bày của em gồm 5 phần. Đầu tiên là bài toán và phạm vi. Tiếp theo là dataset và cách em chuẩn hóa dữ liệu. Phần thứ ba là mô hình, gồm TF-IDF và bốn baseline ML. Sau đó là hệ thống web với Streamlit, inference, storage và feedback. Cuối cùng em sẽ demo hai case đã chuẩn bị để minh họa reliable và suspicious behavior."

Không nói quá lâu ở slide này. Chỉ định hướng cho hội đồng biết flow.

## Slide 3 - Problem and Project Boundary

Nói:

"Vấn đề xuất phát từ việc người dùng tiếng Việt gặp nhiều nội dung thiếu độ tin cậy: tin giật gân, clickbait, bài đăng không rõ nguồn hoặc lan truyền trên mạng xã hội. Nếu hệ thống chỉ trả về fake hoặc real thì người dùng khó tin tưởng, vì họ không biết vì sao hệ thống kết luận như vậy.

Vì vậy phạm vi của đồ án là screening các tín hiệu ngôn ngữ về độ tin cậy. Hệ thống không kiểm chứng sự thật ở mức claim-level, mà hỗ trợ người dùng nhận diện rủi ro ban đầu qua risk score, suspicious terms, explanation, history và feedback."

Nếu thầy hỏi boundary:

"Dạ boundary của em là linguistic reliability screening, chưa phải full fact-checking có evidence retrieval."

## Slide 4 - Objectives and Contributions

Nói:

"Mục tiêu của đồ án gồm bốn phần: xây dựng web app, huấn luyện và so sánh các mô hình supervised ML, trực quan hóa risk và tín hiệu đáng nghi, và thu thập feedback cho hướng retraining sau này.

Về đóng góp, em có một pipeline tái lập được từ download, clean, split, train, evaluate. Em benchmark bốn mô hình và chọn best model bằng metric. Phần kết quả có explainability gồm ML risk, lexical risk, highlighted terms và token contribution. Về kiến trúc, hệ thống tách thành Streamlit UI, NLP/ML core và Supabase/PostgreSQL."

Câu nhấn mạnh:

"Điểm em muốn bảo vệ là workflow ML hoàn chỉnh, không chỉ một giao diện nhập text."

## Slide 5 - Dataset and Label Convention

Nói:

"Nguồn dữ liệu chính là VFND Vietnamese Fake News Dataset. Đây là dataset phục vụ nghiên cứu fake news tiếng Việt. Trong project, em chuẩn hóa nhãn về bài toán binary reliability screening.

Quy ước nhãn là 0 tương ứng reliable hoặc real news, còn 1 tương ứng unreliable, fake hoặc clickbait. Sau khi xử lý, dữ liệu được chia thành 350 mẫu train, 75 mẫu validation và 75 mẫu test."

Nếu mở web dataset:

"Em mở nguồn GitHub dataset để chứng minh traceability. Còn trong project, dữ liệu đã được tải, làm sạch và lưu thành các split local để train model tái lập được."

Nếu thầy hỏi dataset nhỏ:

"Dạ dataset còn nhỏ, nên em chọn baseline dễ tái lập và giải thích được, không tuyên bố hệ thống kiểm chứng sự thật tuyệt đối."

## Slide 6 - Data Preparation Evidence

Nói:

"Bước chuẩn bị dữ liệu là một phần quan trọng của đồ án. Em loại bỏ missing labels, text không dùng được, các bản ghi trùng lặp và các văn bản quá ngắn. Duplicate ratio bị loại bỏ khoảng 31.32%, threshold độ dài tối thiểu là 20 ký tự.

Sau xử lý, label distribution khá cân bằng: 251 mẫu label 0 và 249 mẫu label 1. Điều này giúp các metric như accuracy và F1 macro có ý nghĩa hơn. Việc chia train, validation, test rõ ràng cũng giúp tránh việc đánh giá trên dữ liệu đã dùng để train."

Nếu thầy hỏi vì sao cần validation:

"Validation dùng để chọn model, còn test được giữ lại để đánh giá cuối cùng."

## Slide 7 - NLP and ML Pipeline

Nói:

"Pipeline của em đi từ raw dataset đến exported model artifact. Đầu tiên là download dataset. Sau đó clean dữ liệu, chuẩn hóa nhãn, loại duplicate và short texts. Tiếp theo là split train, validation và test.

Ở bước train, em dùng TF-IDF kết hợp bốn supervised baselines. Sau đó đánh giá bằng F1 macro, accuracy, ROC-AUC và confusion matrix. Cuối cùng, best model được export thành file joblib cùng metadata để tích hợp vào web app."

Câu nói thêm:

"Khi demo app, app không train lại từ đầu. App chỉ load model đã train để inference nhanh và ổn định."

## Slide 8 - Methodology Choices

Nói:

"Em chọn TF-IDF vì dữ liệu hiện tại còn nhỏ, cần phương pháp nhanh, ổn định và dễ giải thích. TF-IDF biến văn bản thành vector số, trong đó mỗi chiều tương ứng với một từ hoặc cụm từ. Trọng số cao khi từ đó quan trọng trong văn bản nhưng không quá phổ biến trong toàn bộ dataset.

Trong project, TF-IDF dùng cả unigram và bigram. Unigram là từ đơn như 'sốc', còn bigram là cụm hai từ như 'tin đồn' hoặc 'chưa kiểm'. Bigram quan trọng vì nhiều tín hiệu tin giả/clickbait nằm ở cụm từ chứ không chỉ từ đơn."

Giải thích 4 model:

"Em train bốn baseline. Logistic Regression là baseline tuyến tính có xác suất. Linear SVM là mô hình margin-based, thường mạnh với TF-IDF thưa và nhiều chiều. Random Forest là tree ensemble để so sánh hướng phi tuyến. Naive Bayes là baseline cổ điển, train nhanh cho bài toán text classification."

Nếu thầy hỏi vì sao chưa dùng PhoBERT:

"Với dataset nhỏ, TF-IDF + Linear SVM ổn định và dễ giải thích hơn. PhoBERT là hướng phát triển khi có dataset lớn hơn và GPU ổn định."

## Slide 9 - Model Benchmark

Nói:

"Slide này trình bày kết quả benchmark bốn mô hình. Em chọn best model theo validation F1 macro, không chọn theo cảm tính. Kết quả cho thấy Linear SVM có validation F1 macro cao nhất là 0.9466, nên được chọn làm best model.

Ở test set trong bảng benchmark, Linear SVM cũng đạt F1 macro 0.9064, cao hơn các model còn lại trong bảng này. Sau khi chọn SVM, em refit best model trên train plus validation; kết quả cuối trong metadata/report đạt accuracy khoảng 0.92 và F1 macro khoảng 0.9199."

Nếu thầy hỏi F1 macro là gì:

"F1 macro tính F1 riêng cho từng lớp rồi lấy trung bình, nên hai lớp reliable và unreliable được xem công bằng như nhau."

## Slide 10 - Best Model Evaluation

Nói:

"Đây là phần đánh giá best model. Em dùng confusion matrix để nhìn rõ model dự đoán đúng và sai trên từng lớp, thay vì chỉ nhìn accuracy.

Linear SVM phù hợp ở đây vì TF-IDF tạo ra vector thưa và nhiều chiều. Trong không gian đó, Linear SVM thường tìm được ranh giới phân tách tốt. Ngoài ra, việc dùng macro F1 giúp đánh giá công bằng cả reliable và unreliable."

Nếu thầy hỏi model sai thì sao:

"Các lỗi trong confusion matrix là cơ sở để phân tích error cases. Trong app, em có feedback form để người dùng đánh dấu đúng/sai/không chắc, phục vụ review và retraining sau này."

## Slide 11 - Layered Architecture

Nói:

"Hệ thống được thiết kế theo layered architecture. Presentation layer là Streamlit UI, chịu trách nhiệm nhập văn bản, hiển thị dashboard, history và feedback.

Core engine gồm preprocessing, TF-IDF, inference, risk scoring và explanation. Data layer dùng Supabase/PostgreSQL, có local fallback nếu cloud không khả dụng. Artifacts là model đã export như best_model.joblib và metadata."

Câu nhấn mạnh:

"Việc tách lớp giúp hệ thống dễ bảo trì. Nếu sau này thay Linear SVM bằng PhoBERT, em chỉ cần thay core engine và model artifact, không phải viết lại toàn bộ UI."

## Slide 12 - Prediction Workflow

Nói:

"Workflow bắt đầu từ input, có thể là text hoặc URL được hỗ trợ. Sau đó hệ thống preprocess để normalize, clean và validate text. Tiếp theo, text đi qua TF-IDF và Linear SVM để inference.

Sau inference, hệ thống tạo explanation gồm risk, token contribution và highlight. Kết quả được persist vào Supabase hoặc local fallback. Cuối cùng, người dùng có thể gửi feedback correct, incorrect hoặc uncertain."

Câu nói thêm:

"Đây là lý do em nói hệ thống là workflow hỗ trợ review, không chỉ là một textbox trả điểm."

## Slide 13 - Application Result and Explainability

Nói:

"Slide này minh họa trang kết quả của app. Em thiết kế kết quả theo hướng readable review. Người dùng thấy assessment, risk band, risk score, ML risk, lexical risk, highlighted input, suspicious signals và model explanation.

Điểm quan trọng là explainability. Suspicious terms giúp thấy các từ/cụm từ đáng nghi như 'sốc', 'tin đồn', 'chưa kiểm chứng'. Token contribution cho thấy token nào đẩy mô hình về phía reliable hoặc unreliable."

Nếu thầy hỏi token contribution là gì:

"Với model tuyến tính, contribution có thể hiểu là TF-IDF value nhân với trọng số model. Contribution dương đẩy về unreliable, contribution âm đẩy về reliable."

## Slide 14 - Database and Feedback Loop

Nói:

"Supabase/PostgreSQL được dùng để lưu prediction history và feedback. Prediction record gồm input text, model output, risk score, explanation và created time. Feedback gồm user judgment, optional note và prediction id liên kết.

Nhờ đó hệ thống có history cho reviewer xem lại và có dữ liệu feedback phục vụ retraining trong tương lai. Nếu Supabase không khả dụng, app có local fallback để demo không bị gián đoạn."

Nếu thầy hỏi feedback dùng làm gì:

"Feedback không tự động retrain ngay trong bản hiện tại, nhưng là nguồn dữ liệu để reviewer kiểm tra, làm sạch và đưa vào lần retraining sau."

## Slide 15 - Limitations and Future Work

Nói:

"Em trình bày limitation rõ ràng vì đây là bài toán khó. Hạn chế hiện tại là dataset còn nhỏ, hệ thống mới screening tín hiệu ngôn ngữ chứ chưa chứng minh sự thật tuyệt đối, chưa có claim-level evidence retrieval và chưa mô hình hóa source credibility đầy đủ.

Hướng phát triển là mở rộng dataset tiếng Việt, fine-tune PhoBERT hoặc mô hình ngôn ngữ tiếng Việt khác, thêm source credibility, claim evidence retrieval và dùng feedback data cho monitored retraining."

Câu nhấn mạnh:

"Nói limitation không làm đồ án yếu hơn; nó cho thấy em hiểu đúng phạm vi và biết hướng phát triển."

## Slide 16 - Conclusion

Nói:

"Tóm lại, đồ án đã xây dựng được một hệ thống NLP/ML có thể tái lập, giải thích được và có khả năng mở rộng. Sản phẩm gồm web app Streamlit, pipeline ML từ dataset cleaning đến TF-IDF và bốn baseline, metrics và exported model.

Phần explainability gồm risk score, lexical signals, highlighted terms và token contribution. Phần storage loop dùng Supabase/PostgreSQL để lưu history và feedback."

Câu kết đẹp:

"Điểm chính của đồ án không chỉ là giao diện dự đoán, mà là một workflow ML hoàn chỉnh cho bài toán đánh giá độ tin cậy tin tức tiếng Việt."

## Slide 17 - Thank You

Nói:

"Em xin cảm ơn thầy cô đã lắng nghe. Em sẵn sàng nhận câu hỏi và góp ý từ thầy cô."

Nếu hội đồng hỏi ngay:

- Dataset: trả lời bằng VFND, label convention, train/validation/test.
- Model: trả lời TF-IDF + 4 baseline, chọn Linear SVM bằng validation F1 macro.
- App: trả lời Streamlit + explainability + Supabase history/feedback.
- Limitation: dataset nhỏ, chưa evidence retrieval, future work PhoBERT/source credibility.

## Câu Trả Lời Nhanh Nếu Bị Hỏi Khó

**Có khác gì một trang nhập text trả điểm?**

"Khác ở pipeline và workflow phía sau: dataset được làm sạch, chia train/validation/test, TF-IDF, bốn mô hình benchmark, metrics, confusion matrix, explainability, prediction history, feedback loop và report export."

**Risk score có phải xác suất thật không?**

"Không hoàn toàn. Risk score là decision-support score, kết hợp ML risk và lexical risk để hỗ trợ sàng lọc ban đầu."

**Vì sao chọn SVM?**

"Vì SVM có validation F1 macro cao nhất và phù hợp với TF-IDF sparse high-dimensional vectors."

**Vì sao chưa dùng deep learning?**

"Với dataset nhỏ, baseline TF-IDF + SVM ổn định, tái lập và giải thích được hơn. Deep learning/PhoBERT là future work."

**Nếu model sai thì sao?**

"App có feedback form. Feedback được lưu để reviewer kiểm tra và làm dữ liệu retraining sau này."
