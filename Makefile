PYTHON ?= python
.PHONY: setup data prepare train eval app all

setup:
	$(PYTHON) -m pip install -r requirements.txt

data:
	PYTHONPATH=. $(PYTHON) scripts/download_data.py

prepare:
	PYTHONPATH=. $(PYTHON) scripts/prepare_data.py

train:
	PYTHONPATH=. $(PYTHON) scripts/train_baseline.py

eval:
	PYTHONPATH=. $(PYTHON) scripts/generate_explanations.py --text "Đây là bản tin thử nghiệm để đánh giá độ tin cậy."

app:
	streamlit run app/streamlit_app.py

all: setup data prepare train eval
