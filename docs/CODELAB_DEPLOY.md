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
