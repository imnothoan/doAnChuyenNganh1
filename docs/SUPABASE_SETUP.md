# Supabase Setup

## 1) Tạo biến môi trường
Copy `.env.example` thành `.env` và điền:
- `SUPABASE_URL`
- `SUPABASE_KEY`

## 2) Khởi tạo schema
Chạy SQL trong `scripts/init_supabase.sql` trên Supabase SQL Editor.

Schema gồm:
- `predictions`: lưu text, model, nhãn, confidence, risk score, probability JSON, suspicious terms và explanation.
- `feedback`: lưu đánh giá đúng/sai/không chắc của người dùng để làm dữ liệu tái huấn luyện.

Hoặc chạy bằng connection string PostgreSQL:

```bash
export SUPABASE_DB_URL="postgresql://..."
python3 scripts/setup_supabase_db.py
```

Không commit `SUPABASE_DB_URL`, `service_role` hoặc database password.

## 3) Chế độ fallback
Nếu thiếu key/url hoặc SDK lỗi, hệ thống tự fallback local vào:
- `data/processed/supabase_fallback.jsonl`

## 4) Bảo mật
- Không commit key thật.
- Không hardcode token trong code.
- App chỉ cần anon/publishable key. Service role chỉ dùng cho tác vụ quản trị, không đưa vào `.env` chạy app.
