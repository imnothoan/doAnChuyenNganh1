# CODELAB DEPLOY

## Chạy local Streamlit
```bash
make app
```

## Deploy gợi ý
- Streamlit Community Cloud hoặc Docker.
- Cấu hình biến môi trường từ `.env`.

## Bật/tắt Supabase
- Bật: set `SUPABASE_URL`, `SUPABASE_KEY`
- Tắt: để trống hai biến trên, app vẫn chạy fallback local.

## Bật nhập URL an toàn
- Set `ALLOWED_NEWS_DOMAINS` trong `.env` (comma-separated), ví dụ:
  - `ALLOWED_NEWS_DOMAINS=vnexpress.net,tuoitre.vn`
- Nếu để trống, app sẽ tắt URL fetch để giảm rủi ro SSRF.
