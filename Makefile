PYTHON ?= python3
.PHONY: setup data prepare train eval db app all

setup:
	$(PYTHON) -m pip install -r requirements.txt

data:
	$(PYTHON) scripts/download_data.py

prepare:
	$(PYTHON) scripts/prepare_data.py

train:
	$(PYTHON) scripts/train_baseline.py

eval:
	$(PYTHON) scripts/evaluate.py

db:
	$(PYTHON) scripts/setup_supabase_db.py

app:
	streamlit run app/streamlit_app.py

all: setup data prepare train eval
