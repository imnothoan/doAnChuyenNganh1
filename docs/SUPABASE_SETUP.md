# Supabase Setup

## 1) Tạo biến môi trường
Copy `.env.example` thành `.env` và điền:
- `SUPABASE_URL`
- `SUPABASE_KEY`

## 2) Khởi tạo schema
Chạy SQL trong `scripts/init_supabase.sql` trên Supabase SQL Editor.

## 3) Chế độ fallback
Nếu thiếu key/url hoặc SDK lỗi, hệ thống tự fallback local vào:
- `data/processed/supabase_fallback.jsonl`

## 4) Bảo mật
- Không commit key thật.
- Không hardcode token trong code.
