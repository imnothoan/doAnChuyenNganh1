# Nội Dung Demo Copy/Paste Khi Bảo Vệ

Mục tiêu của file này là giúp buổi demo ổn định mà vẫn tự nhiên. Khi bảo vệ, em mở file này hoặc đưa nội dung vào Google Docs, copy từng case và paste vào ô `Vietnamese news content` trong app.

Không nói đây là dữ liệu train. Hãy nói: "Đây là các ca kiểm thử đã chuẩn bị trước để minh họa hai nhóm hành vi của hệ thống: văn bản có dấu hiệu đáng tin và văn bản có dấu hiệu clickbait/chưa kiểm chứng."

## Case 1 - Văn Bản Có Dấu Hiệu Đáng Tin

### Nội dung để copy

Hơn 55 tỷ đồng nâng cấp 8,5 km đại lộ Võ Văn Kiệt ở TP HCM. Dự án sửa chữa, nâng cao độ mặt đường từ cầu Lò Gốm đến giao lộ Ký Con đang được Trung tâm Quản lý đường hầm sông Sài Gòn triển khai. Dự án có tổng mức đầu tư gần 56,5 tỷ đồng, thời gian thi công 240 ngày. Theo đại diện trung tâm, mục tiêu là đảm bảo an toàn giao thông, giảm ngập và cải thiện mỹ quan đô thị.

### Em nói khi paste case này

"Em bắt đầu với một đoạn tin có phong cách báo chí chính thống: có địa điểm, đơn vị triển khai, số liệu đầu tư, thời gian thi công và mục tiêu cụ thể. Sau khi bấm Analyze, hệ thống dự kiến cho risk thấp hơn vì lexical risk thấp và mô hình không thấy nhiều dấu hiệu clickbait."

### Điểm cần chỉ trên màn hình

- `Assessment Summary`: nhãn và risk band.
- `Risk score`, `ML risk`, `Lexical risk`: giải thích đây là các tín hiệu hỗ trợ quyết định.
- `Why this result?`: giải thích model học từ TF-IDF và lexical rules bắt các từ đáng nghi.
- `Model explanation`: token nào đẩy về reliable/unreliable.

## Case 2 - Văn Bản Có Dấu Hiệu Nghi Ngờ/Clickbait

### Nội dung để copy

SỐC! Tin đồn chưa kiểm chứng lan truyền trên mạng xã hội cho rằng một sự việc kinh hoàng vừa xảy ra và khiến rất nhiều người hoang mang. Bài viết không nêu nguồn tin chính thức, không có tài liệu xác thực, chỉ kêu gọi mọi người chia sẻ ngay trước khi bị xóa. Nội dung dùng nhiều từ như không thể tin, bí mật, chấn động và gây sốt để thu hút tương tác.

### Em nói khi paste case này

"Tiếp theo em dùng một đoạn kiểm thử có nhiều dấu hiệu tin nghi ngờ: từ ngữ cảm xúc mạnh, kêu gọi chia sẻ, không nêu nguồn chính thức và tự nhận là chưa kiểm chứng. Mục tiêu là kiểm tra hệ thống có highlight được lexical signals và đẩy risk lên cao hay không."

### Điểm cần chỉ trên màn hình

- `Suspicious signals`: các cụm đáng nghi như "sốc", "chưa kiểm chứng", "bí mật", "chấn động".
- `Highlighted input`: các từ được tô sáng trực tiếp trong văn bản.
- `Lexical risk`: giải thích vì sao tăng cao.
- `Pushes toward unreliable`: token contribution giúp hệ thống có tính explainability.

## Case 3 - URL Demo Nếu Còn Thời Gian

URL reliable gợi ý:

```text
https://vnexpress.net/sau-cong-nghe-chien-luoc-uu-tien-trien-khai-ngay-5003002.html
```

URL fact-check gợi ý:

```text
https://tuoitre.vn/xe-khach-lat-o-deo-phuong-hoang-lam-18-nguoi-chet-la-tin-gia-cau-view-20260526181200255.htm
```

Khi dùng URL fact-check, phải nói rõ:

"Đây là bài báo chính thống đang nói về một claim giả, nên trong nội dung có thể xuất hiện nhiều từ khóa fake-news. Vì vậy em dùng URL mode để chứng minh chức năng trích xuất nội dung, còn kết luận vẫn phải đọc cùng explanation."

## Thứ Tự Demo Đề Xuất

1. Mở `Dashboard` trước để nói dataset, training, metrics và workflow.
2. Mở `Analyze`, paste Case 1, bấm `Analyze`.
3. Paste Case 2, bấm `Analyze`.
4. Gửi feedback `Correct`.
5. Mở `History` để chứng minh dữ liệu đã lưu.
6. Nếu còn thời gian, demo URL mode.
