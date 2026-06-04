# Ôn Tập Bảo Vệ Chi Tiết - Đồ Án Chuyên Ngành 1

Đề tài: **Machine Learning-based Visual Tool for News Reliability Assessment**

Mục tiêu của file này là giúp em **hiểu thật** để ngày mai có gì cũng có cái để nói. File này không phải kịch bản bấm demo, mà là tài liệu ôn kiến thức: dataset, preprocessing, TF-IDF, model, metrics, risk score, explainability, Supabase, limitations và câu trả lời vấn đáp.

Khi bảo vệ, em không cần nói hết file này. Em dùng file này để học. Lên trình bày thì nói ngắn, rõ, đúng trọng tâm.

## 1. Câu Tóm Tắt Đề Tài Trong 30 Giây

Nếu thầy hỏi "đồ án của em làm gì?", nói:

"Đồ án của em xây dựng một công cụ web hỗ trợ đánh giá độ tin cậy tin tức tiếng Việt. Người dùng nhập một đoạn tin hoặc URL bài báo, hệ thống xử lý văn bản bằng NLP, trích xuất đặc trưng TF-IDF, dùng mô hình học máy đã huấn luyện để dự đoán reliable hoặc unreliable, sau đó hiển thị risk score, các dấu hiệu ngôn ngữ đáng nghi, token contribution, lịch sử phân tích và feedback của người dùng."

Nói ngắn hơn:

"Đây là hệ thống hỗ trợ sàng lọc độ tin cậy tin tức bằng NLP/ML, có giải thích kết quả và feedback loop."

## 2. Vì Sao Đề Tài Không Chỉ Là Một Web Nhập Text?

Nếu thầy nhìn app và nói "cái này chỉ nhập text rồi trả điểm à?", em nói:

"Nếu chỉ nhìn tab Analyze thì giao diện được tối giản để người dùng dễ thao tác. Nhưng phần trọng tâm của đồ án nằm ở pipeline phía sau: dữ liệu được thu thập và làm sạch, chia train/validation/test, trích xuất TF-IDF, huấn luyện 4 mô hình baseline, chọn best model bằng validation F1 macro, đánh giá bằng accuracy/F1/ROC-AUC/confusion matrix, tích hợp vào Streamlit, lưu history và feedback bằng Supabase."

Các điểm chứng minh chiều sâu:

- Có dataset thật: VFND Vietnamese Fake News Dataset.
- Có preprocessing riêng cho tiếng Việt.
- Có TF-IDF vectorization.
- Có 4 mô hình baseline.
- Có model comparison và best model.
- Có metrics thật.
- Có confusion matrix.
- Có explainability: token contribution và suspicious-term highlighting.
- Có database workflow: prediction history và feedback.
- Có notebook Colab để train lại.
- Có report/UML/ERD/architecture diagrams.

## 3. Dataset Em Dùng Là Gì?

Nguồn chính:

```text
https://github.com/WhySchools/VFND-vietnamese-fake-news-datasets
```

Trong project có ghi nguồn ở:

```text
reports/dataset_sources.json
reports/dataset_profile.md
```

Dữ liệu sau xử lý:

- Train: 350 mẫu
- Validation: 75 mẫu
- Test: 75 mẫu
- Label 0: 251 mẫu
- Label 1: 249 mẫu

Quy ước nhãn:

- `0 = reliable / real`
- `1 = unreliable / fake / clickbait`

Câu nói khi trình bày:

"Nguồn dữ liệu chính của em là VFND, một dataset tiếng Việt phục vụ nghiên cứu fake news. Em chuẩn hóa nhãn về 0 là reliable/real và 1 là unreliable/fake/clickbait. Sau bước làm sạch, dữ liệu được chia thành train, validation và test. Em dùng validation để chọn mô hình tốt nhất, còn test để đánh giá cuối cùng."

Nếu thầy hỏi "dataset nhỏ không?":

"Dạ dataset còn nhỏ, đây là hạn chế của đồ án. Vì vậy em chọn các baseline truyền thống như TF-IDF + Linear SVM để đảm bảo hệ thống chạy ổn định, dễ tái lập và dễ giải thích. Hướng phát triển là mở rộng dataset và thử PhoBERT khi có dữ liệu lớn hơn."

## 4. Preprocessing Làm Những Gì?

Trong code, preprocessing nằm ở:

```text
src/features/text_preprocessing.py
```

Các bước chính:

1. Chuẩn hóa Unicode theo dạng NFC để tiếng Việt có dấu ổn định.
2. Xóa URL trong text.
3. Chuẩn hóa khoảng trắng.
4. Chuyển text về lowercase khi tokenize.
5. Loại bỏ dấu câu trong bước tokenization.
6. Tách token bằng regex.
7. Loại bỏ stopwords tiếng Việt tự định nghĩa.
8. Bỏ token có độ dài <= 1.
9. Giữ lại dấu tiếng Việt, không chuyển "điện" thành "dien".

Câu nói:

"Ở bước preprocessing, em không làm mất dấu tiếng Việt vì dấu là thông tin quan trọng. Em chuẩn hóa Unicode, loại bỏ URL, chuẩn hóa khoảng trắng, chuyển lowercase, loại bỏ dấu câu khi tokenize, bỏ stopwords và các token quá ngắn. Kết quả đầu ra là chuỗi token sạch để đưa vào TF-IDF."

Ví dụ:

Input:

```text
SỐC! Tin đồn chưa kiểm chứng lan truyền trên mạng xã hội.
```

Sau preprocessing có thể còn các token quan trọng như:

```text
sốc tin đồn kiểm chứng lan truyền mạng xã hội
```

Lưu ý: stopwords như "và", "là", "của", "trong" bị loại vì thường ít mang ý nghĩa phân loại.

## 5. TF-IDF Là Gì?

TF-IDF là viết tắt của:

- **TF = Term Frequency**: một từ xuất hiện nhiều trong văn bản thì TF cao.
- **IDF = Inverse Document Frequency**: từ nào xuất hiện quá phổ biến trong toàn bộ dataset thì IDF thấp; từ nào đặc trưng hơn thì IDF cao.

Công thức ý tưởng:

```text
TF-IDF(word, document) = TF(word, document) * IDF(word)
```

Hiểu đơn giản:

- Từ xuất hiện trong bài hiện tại nhiều -> có thể quan trọng.
- Nhưng nếu từ đó xuất hiện ở hầu hết mọi bài -> không còn đặc trưng.
- TF-IDF tăng trọng số cho từ vừa xuất hiện trong bài, vừa có tính phân biệt giữa các bài.

Ví dụ:

- Các từ như "và", "là", "của" xuất hiện nhiều ở mọi bài -> ít giá trị phân loại.
- Các cụm như "tin đồn", "chưa kiểm chứng", "sốc", "chấn động" có thể mang tín hiệu đáng nghi.
- Các cụm về cơ quan, dự án, số liệu, địa điểm có thể gần với phong cách tin chính thống hơn.

Câu nói:

"Em dùng TF-IDF để biến văn bản thành vector số. Mỗi chiều của vector tương ứng với một từ hoặc cụm từ. Trọng số TF-IDF thể hiện mức độ quan trọng của từ đó trong văn bản so với toàn bộ tập dữ liệu. Nhờ vậy mô hình học máy có thể xử lý văn bản bằng số."

## 6. Cấu Hình TF-IDF Trong Project

Trong code:

```text
src/models/train_baseline.py
```

Cấu hình:

```python
TfidfVectorizer(
    max_features=50000,
    ngram_range=(1, 2),
    min_df=1,
    max_df=0.95,
    sublinear_tf=True,
    lowercase=False,
    preprocessor=preprocess_for_ml,
    token_pattern=r"(?u)\b\w+\b",
)
```

Giải thích từng tham số:

- `max_features=50000`: chỉ giữ tối đa 50.000 đặc trưng quan trọng nhất để tránh vector quá lớn.
- `ngram_range=(1, 2)`: dùng cả unigram và bigram.
- `unigram`: từ đơn, ví dụ `sốc`, `tin`, `đồn`.
- `bigram`: cụm 2 từ, ví dụ `tin đồn`, `chưa kiểm`, `kiểm chứng`.
- `min_df=1`: từ/cụm xuất hiện ít nhất 1 document vẫn được xét.
- `max_df=0.95`: bỏ những từ xuất hiện trong hơn 95% document vì quá phổ biến.
- `sublinear_tf=True`: dùng `1 + log(tf)` thay vì TF thô, giúp giảm ảnh hưởng của từ lặp quá nhiều.
- `lowercase=False`: vì project đã tự xử lý lowercase trong `preprocess_for_ml`.
- `preprocessor=preprocess_for_ml`: dùng hàm preprocessing tiếng Việt của project.
- `token_pattern`: regex để nhận token Unicode, phù hợp tiếng Việt.

Câu nói:

"Em cấu hình TF-IDF dùng cả unigram và bigram để mô hình học được cả từ đơn và cụm từ. Ví dụ từ 'sốc' là unigram, còn 'tin đồn' hoặc 'chưa kiểm chứng' là bigram có ý nghĩa mạnh hơn. Em giới hạn 50.000 features để cân bằng giữa độ biểu diễn và hiệu năng."

Nếu thầy hỏi "tại sao dùng bigram?":

"Vì trong tiếng Việt và trong tin tức, nhiều tín hiệu nằm ở cụm từ chứ không chỉ từ đơn. Ví dụ 'tin' riêng lẻ chưa chắc đáng nghi, nhưng 'tin đồn' lại là tín hiệu khác. Bigram giúp mô hình bắt được các cụm như vậy."

## 7. Vì Sao Không Dùng Word Embedding/PhoBERT Ngay?

Câu trả lời:

"Với dataset hiện tại còn nhỏ và yêu cầu đồ án cần chạy ổn định, em chọn TF-IDF + baseline models trước. TF-IDF nhanh, dễ tái lập, dễ giải thích và phù hợp để chứng minh pipeline ML hoàn chỉnh. PhoBERT hoặc deep learning là hướng phát triển khi có dataset lớn hơn và tài nguyên GPU ổn định hơn."

Nếu muốn nói mạnh hơn:

"Em không chọn mô hình phức tạp chỉ để làm hệ thống trông hiện đại. Em ưu tiên mô hình phù hợp với dữ liệu, có metrics rõ ràng và giải thích được khi bảo vệ."

## 8. Em Train Những Model Nào?

Project train 4 model:

1. Logistic Regression
2. Linear SVM
3. Random Forest
4. Multinomial Naive Bayes

Mỗi model được đặt trong một `Pipeline`:

```text
TF-IDF vectorizer -> classifier
```

Nghĩa là khi train hoặc predict, text luôn đi qua TF-IDF trước, rồi mới vào mô hình phân loại.

## 9. Logistic Regression Là Gì?

Nói đơn giản:

"Logistic Regression là mô hình tuyến tính dùng để phân loại. Nó học trọng số cho từng feature TF-IDF, sau đó tính xác suất một văn bản thuộc lớp reliable hoặc unreliable."

Trong project:

```python
LogisticRegression(
    max_iter=1000,
    class_weight="balanced",
    random_state=42
)
```

Giải thích:

- `max_iter=1000`: cho model đủ vòng lặp để hội tụ.
- `class_weight="balanced"`: cân bằng trọng số lớp nếu dữ liệu bị lệch nhãn.
- `random_state=42`: giúp kết quả tái lập.

Nếu thầy hỏi:

"Logistic Regression là baseline tuyến tính, dễ hiểu, có xác suất và thường dùng để so sánh trong text classification."

## 10. Linear SVM Là Gì?

Nói đơn giản:

"Linear SVM là mô hình tìm một đường hoặc siêu phẳng phân tách hai lớp sao cho margin giữa hai lớp lớn nhất. Với dữ liệu TF-IDF nhiều chiều và thưa, Linear SVM thường hoạt động rất tốt."

Trong project:

```python
LinearSVC(
    class_weight="balanced",
    random_state=42
)
```

Vì sao SVM là best model?

- TF-IDF tạo vector có rất nhiều chiều.
- Mỗi văn bản chỉ có một phần nhỏ từ/cụm từ xuất hiện -> vector thưa.
- Linear SVM phù hợp với không gian thưa, nhiều chiều.
- Trong kết quả thực nghiệm, SVM có validation F1 macro cao nhất.

Câu nói:

"Em chọn Linear SVM không phải vì cảm tính. Em train 4 model và chọn best model bằng validation F1 macro. Kết quả SVM cao nhất nên được export thành `baseline_best.joblib` để app sử dụng."

## 11. Random Forest Là Gì?

Nói đơn giản:

"Random Forest là mô hình ensemble gồm nhiều cây quyết định. Mỗi cây học một phần dữ liệu/đặc trưng, sau đó mô hình tổng hợp kết quả từ nhiều cây để dự đoán."

Trong project:

```python
RandomForestClassifier(
    n_estimators=300,
    class_weight="balanced_subsample",
    random_state=42,
    n_jobs=-1
)
```

Giải thích:

- `n_estimators=300`: dùng 300 cây.
- `balanced_subsample`: cân bằng lớp theo từng mẫu bootstrap.
- `n_jobs=-1`: dùng nhiều CPU để train nhanh hơn.

Nếu thầy hỏi "Random Forest có hợp với TF-IDF không?":

"Random Forest không phải mô hình mạnh nhất cho dữ liệu TF-IDF thưa, nhưng em đưa vào để so sánh với hướng phi tuyến/tree-based. Kết quả cho thấy Linear SVM phù hợp hơn trong bài toán này."

## 12. Multinomial Naive Bayes Là Gì?

Nói đơn giản:

"Naive Bayes là mô hình xác suất dựa trên định lý Bayes, thường dùng trong phân loại văn bản. Nó giả định các feature độc lập có điều kiện theo nhãn."

Trong project:

```python
MultinomialNB(alpha=0.5)
```

Giải thích:

- `alpha=0.5`: smoothing để tránh xác suất bằng 0 khi gặp từ chưa xuất hiện trong một lớp.

Nếu thầy hỏi:

"Naive Bayes là baseline kinh điển cho bag-of-words/TF-IDF, train rất nhanh. Em dùng nó để có một mốc so sánh cổ điển trong text classification."

## 13. Vì Sao Train 4 Model?

Câu trả lời:

"Em train 4 model để có benchmark khách quan. Nếu chỉ train một model thì không chứng minh được lựa chọn đó là hợp lý. Em dùng validation F1 macro để chọn best model, sau đó refit best model trên train + validation và đánh giá cuối trên test."

Quy trình:

1. Train từng model trên train set.
2. Đánh giá trên validation set.
3. Chọn model có validation F1 macro cao nhất.
4. Refit best model trên train + validation.
5. Đánh giá cuối trên test set.
6. Export `baseline_best.joblib`.

## 14. Kết Quả Model

Model comparison:

| Model | Val Acc | Val F1 Macro | Test Acc | Test F1 Macro | Test ROC-AUC |
|---|---:|---:|---:|---:|---:|
| Logistic Regression | 0.9200 | 0.9196 | 0.8933 | 0.8929 | 0.9772 |
| Linear SVM | 0.9467 | 0.9466 | 0.9067 | 0.9064 | 0.9879 |
| Random Forest | 0.9200 | 0.9196 | 0.8933 | 0.8929 | 0.9851 |
| Naive Bayes | 0.9067 | 0.9061 | 0.8933 | 0.8929 | 0.9744 |

Sau khi refit best model:

- Accuracy: 0.9200
- Precision macro: 0.9214
- Recall macro: 0.9196
- F1 macro: 0.9199
- ROC-AUC: 0.9915

Câu nói:

"SVM có validation F1 macro cao nhất nên được chọn làm best model. Sau khi refit trên train + validation, model đạt accuracy khoảng 0.92 và F1 macro khoảng 0.9199 trên test set."

## 15. Metrics Nghĩa Là Gì?

### Accuracy

Tỷ lệ dự đoán đúng trên tổng số mẫu.

```text
Accuracy = số dự đoán đúng / tổng số mẫu
```

Nhược điểm: nếu dữ liệu lệch nhãn, accuracy có thể gây hiểu nhầm.

### Precision

Trong các mẫu model dự đoán là một lớp, có bao nhiêu mẫu thật sự đúng lớp đó.

Nói đơn giản:

"Precision trả lời câu hỏi: khi model cảnh báo unreliable, cảnh báo đó đúng bao nhiêu phần."

### Recall

Trong các mẫu thật sự thuộc một lớp, model tìm ra được bao nhiêu.

Nói đơn giản:

"Recall trả lời câu hỏi: trong các tin unreliable thật, model bắt được bao nhiêu."

### F1-score

F1 là trung bình điều hòa giữa precision và recall.

Nói đơn giản:

"F1 cân bằng giữa precision và recall, phù hợp khi mình không muốn chỉ tối ưu một phía."

### Macro average

Tính metric riêng cho từng lớp rồi lấy trung bình.

Nói đơn giản:

"F1 macro giúp hai lớp reliable và unreliable có trọng số ngang nhau, nên phù hợp khi em muốn đánh giá công bằng cả hai lớp."

### ROC-AUC

Đo khả năng mô hình phân biệt hai lớp trên nhiều ngưỡng khác nhau.

Nói đơn giản:

"ROC-AUC càng cao thì model càng có khả năng xếp mẫu unreliable cao hơn mẫu reliable về mặt điểm rủi ro."

## 16. Confusion Matrix Đọc Như Thế Nào?

Confusion matrix cho biết:

- Reliable thật được dự đoán reliable bao nhiêu.
- Reliable thật bị dự đoán unreliable bao nhiêu.
- Unreliable thật được dự đoán unreliable bao nhiêu.
- Unreliable thật bị dự đoán reliable bao nhiêu.

Câu nói:

"Em dùng confusion matrix để không chỉ nhìn một con số accuracy. Nó giúp thấy model sai ở lớp nào nhiều hơn, từ đó phân tích lỗi và định hướng cải thiện."

## 17. Inference Trong App Chạy Như Thế Nào?

Khi người dùng bấm `Analyze`, app làm:

1. Lấy text từ ô nhập hoặc URL.
2. Làm sạch bằng `basic_clean_text`.
3. Đưa text vào model pipeline.
4. Model pipeline tự chạy TF-IDF rồi classifier.
5. Lấy model probability hoặc decision score.
6. Tính lexical risk từ suspicious terms và punctuation.
7. Tính final risk score.
8. Hiển thị label, risk band, metrics, highlight, token explanation.
9. Lưu prediction vào Supabase hoặc local fallback.
10. Cho phép user gửi feedback.

Câu nói:

"App không train lại model khi người dùng bấm Analyze. Model đã được train trước và export thành file joblib. Khi app chạy, model được load bằng cache để inference nhanh hơn."

## 18. Risk Score Tính Như Thế Nào?

Trong code:

```python
risk_score = max(model_probabilities["unreliable"], lexical_risk)
predicted_label = unreliable if risk_score >= 0.5 else reliable
```

Nghĩa là:

- `ML risk`: rủi ro do mô hình học máy dự đoán.
- `Lexical risk`: rủi ro từ từ khóa đáng nghi, dấu chấm than, dấu hỏi, chữ hoa.
- `Final risk`: lấy mức rủi ro cao hơn giữa hai nguồn tín hiệu.

Vì sao lấy `max`?

"Em dùng cách conservative scoring. Nếu mô hình ML chưa cảnh báo cao nhưng văn bản có quá nhiều dấu hiệu clickbait rõ ràng, hệ thống vẫn tăng risk để hỗ trợ sàng lọc."

Nếu thầy hỏi "risk score có phải xác suất thật không?":

"Không hoàn toàn. Risk score là điểm hỗ trợ quyết định, kết hợp tín hiệu từ mô hình và lexical rules. Nó không phải xác suất tuyệt đối của sự thật."

## 19. Lexical Risk Tính Như Thế Nào?

Project có danh sách suspicious terms:

- Clickbait: `sốc`, `không thể tin`, `bí mật`, `kinh hoàng`, `chấn động`, `gây sốt`, ...
- Emotion: `phẫn nộ`, `hoang mang`, `lo sợ`, `rúng động`, ...
- Credibility: `chưa kiểm chứng`, `tin đồn`, `ẩn danh`, `không rõ nguồn`, `lan truyền`, ...

Trọng số:

- Credibility: 0.22
- Clickbait: 0.16
- Emotion: 0.12
- Dấu chấm than: mỗi dấu +0.04, tối đa 0.12
- Dấu hỏi: mỗi dấu +0.025, tối đa 0.075
- Uppercase ratio: cộng tối đa 0.1
- Lexical risk bị chặn tối đa ở 0.95

Câu nói:

"Lexical risk là lớp tín hiệu rule-based bổ sung cho model. Nó giúp hệ thống phát hiện các dấu hiệu bề mặt như từ giật gân, tin đồn, chưa kiểm chứng hoặc dùng quá nhiều dấu chấm than."

## 20. Explainability Là Gì?

Explainability trong project gồm 2 phần:

1. Suspicious-term highlighting
2. Token contribution từ TF-IDF và trọng số model

### Suspicious-term highlighting

App tìm các cụm đáng nghi và tô sáng trong văn bản.

Ví dụ:

- `sốc`
- `tin đồn`
- `chưa kiểm chứng`
- `không rõ nguồn`
- `chấn động`

### Token contribution

Với model tuyến tính như Logistic Regression hoặc Linear SVM, model có trọng số cho từng feature.

Contribution được tính ý tưởng:

```text
contribution = TF-IDF value * model weight
```

- Contribution dương: đẩy về phía unreliable.
- Contribution âm: đẩy về phía reliable.

Câu nói:

"Phần token contribution giúp hệ thống không bị xem như black box. Người dùng có thể thấy token nào đang đẩy dự đoán về reliable hoặc unreliable."

Nếu thầy hỏi "Random Forest thì giải thích thế nào?":

"Với model phi tuyến như Random Forest, token contribution tuyến tính không áp dụng trực tiếp. Vì vậy app fallback sang hiển thị các TF-IDF input tokens nổi bật. Best model của em là Linear SVM nên token contribution vẫn có ý nghĩa trong demo chính."

## 21. Supabase Dùng Để Làm Gì?

Supabase/PostgreSQL dùng để:

- Lưu prediction history.
- Lưu feedback của người dùng.
- Tạo feedback loop cho retraining sau này.

Trong code:

```text
src/data/supabase_client.py
```

Nếu có `SUPABASE_URL` và `SUPABASE_KEY`, app ghi lên Supabase.

Nếu Supabase lỗi hoặc chưa cấu hình, app ghi vào:

```text
data/processed/supabase_fallback.jsonl
```

Câu nói:

"Supabase giúp hệ thống có lớp dữ liệu tập trung. Mỗi lần người dùng phân tích, prediction được lưu lại. Người dùng có thể gửi feedback đúng, sai hoặc không chắc. Feedback này là nguồn để reviewer kiểm tra và dùng cho retraining trong tương lai."

## 22. Kiến Trúc Phân Lớp Giải Thích Như Nào?

Hệ thống gồm 3 lớp:

### Frontend

- Streamlit
- Nhập text/URL
- Hiển thị dashboard, kết quả, biểu đồ, history, feedback

### Core Engine

- Preprocessing
- TF-IDF vectorization
- Model inference
- Risk scoring
- Explainability

### Database

- Supabase/PostgreSQL
- Lưu predictions
- Lưu feedback

Câu nói:

"Em tách hệ thống theo layered architecture để dễ bảo trì. Nếu sau này thay model SVM bằng PhoBERT, em chỉ cần thay core engine, không phải viết lại toàn bộ UI và database."

## 23. URL Mode Nên Nói Như Thế Nào?

URL mode chỉ là chức năng hỗ trợ.

Câu nói:

"URL mode dùng để trích xuất nội dung từ bài báo thuộc allowed domains. Tuy nhiên kết quả vẫn phải đọc cùng explanation. Đặc biệt với bài fact-check, nội dung có thể chứa nhiều từ khóa fake-news vì bài đó đang nói về một claim giả."

Không nói:

"URL này là fake."

Nói đúng:

"Bài này có thể là bài chính thống đang bàn về một claim giả, nên cần đọc explanation."

## 24. Những Câu Thầy Có Thể Hỏi Và Cách Trả Lời

### Dataset lấy ở đâu?

"Dạ dataset chính là VFND Vietnamese Fake News Dataset trên GitHub. Em mở nguồn dataset để chứng minh. Sau đó em xử lý thành train/validation/test trong project."

### Label có đáng tin không?

"Nhãn dựa trên dataset gốc Fake/Real. Em chuẩn hóa lại thành reliable/unreliable. Chất lượng nhãn phụ thuộc dataset gốc, nên em có trình bày limitation và không khẳng định hệ thống kiểm chứng sự thật tuyệt đối."

### Tại sao dùng TF-IDF?

"Vì TF-IDF phù hợp với baseline text classification, nhanh, dễ tái lập, dễ giải thích và hoạt động tốt với dataset nhỏ. Nó giúp biến văn bản thành vector số để các mô hình ML xử lý được."

### Tại sao chọn Linear SVM?

"Vì em so sánh 4 model và SVM có validation F1 macro cao nhất. Ngoài ra SVM thường mạnh với dữ liệu TF-IDF thưa, nhiều chiều."

### Tại sao không dùng deep learning?

"Với dataset hiện tại còn nhỏ, deep learning dễ overfit và khó giải thích hơn. Em ưu tiên baseline ổn định, tái lập được và explainable. PhoBERT là hướng phát triển."

### App này giúp người dùng quyết định gì?

"App giúp người dùng sàng lọc ban đầu: bài nào có risk cao, có dấu hiệu clickbait, có từ khóa chưa kiểm chứng thì cần kiểm tra thêm nguồn và bằng chứng."

### Nếu model sai thì sao?

"App có feedback form. Người dùng có thể đánh dấu đúng/sai/không chắc. Feedback được lưu để reviewer kiểm tra và dùng cho retraining."

### Có khác gì trang nhập text trả điểm?

"Khác ở pipeline và workflow: dataset, preprocessing, TF-IDF, benchmark 4 model, metrics, confusion matrix, explanation, history, feedback và report export."

## 25. Nếu Em Run Quá, Chỉ Cần Nhớ 7 Ý Này

1. Đề tài là decision-support tool, không phải fact-checker tuyệt đối.
2. Dataset chính là VFND tiếng Việt.
3. Label: 0 reliable/real, 1 unreliable/fake/clickbait.
4. Preprocessing giữ dấu tiếng Việt, loại URL, stopwords, dấu câu, token ngắn.
5. TF-IDF biến text thành vector số, dùng unigram + bigram.
6. Train 4 model, chọn Linear SVM bằng validation F1 macro.
7. App có explainability, history và feedback loop.

## 26. Câu Kết Luận Đẹp

"Tóm lại, đồ án của em không chỉ xây dựng giao diện dự đoán, mà xây dựng một pipeline ML hoàn chỉnh cho bài toán đánh giá độ tin cậy tin tức tiếng Việt: từ dataset, preprocessing, TF-IDF, huấn luyện và benchmark mô hình, đến web inference, giải thích kết quả, lưu lịch sử và thu thập feedback. Hạn chế hiện tại là dataset còn nhỏ và chưa có evidence retrieval, nhưng kiến trúc đã sẵn sàng để mở rộng sang PhoBERT, source credibility và claim-level fact-checking trong tương lai."
