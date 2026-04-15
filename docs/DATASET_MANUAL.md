# Dataset Manual Download Guide

Các nguồn không tải tự động được. Hãy tải thủ công và đặt vào `data/raw/<dataset_name>/`.

## Danh sách lỗi
- Dataset: Zenodo
  - URL: https://zenodo.org/records/2578917/latest
  - Lỗi: Zenodo latest endpoint may require browser/manual download
  - Đích mong muốn: /home/runner/work/doAnChuyenNganh1/doAnChuyenNganh1/data/raw/zenodo

## Bước thủ công
1. Tải file/clone repo từ URL tương ứng.
2. Giải nén nếu cần và đặt vào thư mục `data/raw/` theo tên dataset.
3. Chạy lại `make prepare`.
4. Kiểm tra `reports/dataset_sources.json` để xác nhận trạng thái.