#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if [[ ! -d ".venv" ]]; then
  echo "❌ Không tìm thấy .venv. Hãy tạo trước:"
  echo "python3 -m venv .venv"
  exit 1
fi

source .venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

export PYTHONPATH="$ROOT_DIR"

python3 scripts/download_data.py
python3 scripts/prepare_data.py
python3 scripts/train_baseline.py
python3 scripts/evaluate.py

echo ""
echo "✅ Output checklist:"
for f in \
  data/processed/train.csv \
  data/processed/val.csv \
  data/processed/test.csv \
  models/artifacts/baseline_lr.joblib \
  models/artifacts/baseline_svm.joblib \
  reports/metrics_baseline.json \
  reports/model_comparison.md \
  reports/figures/confusion_matrix_lr.png \
  reports/figures/confusion_matrix_svm.png \
  reports/figures/confusion_matrix_nb.png
do
  if [[ -f "$f" ]]; then
    echo "  [x] $f"
  else
    echo "  [ ] $f (missing)"
  fi
done
