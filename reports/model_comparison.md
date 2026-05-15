# Model Comparison

Best model selected by validation F1 macro: **svm**.

Label convention: `0 = reliable/real`, `1 = unreliable/fake/clickbait`.

| Model | Val Acc | Val F1 Macro | Test Acc | Test F1 Macro | Test ROC-AUC |
|---|---:|---:|---:|---:|---:|
| lr | 0.9200 | 0.9196 | 0.8933 | 0.8929 | 0.9772 |
| svm | 0.9467 | 0.9466 | 0.9067 | 0.9064 | 0.9879 |
| rf | 0.9200 | 0.9196 | 0.8933 | 0.8929 | 0.9851 |
| nb | 0.9067 | 0.9061 | 0.8933 | 0.8929 | 0.9744 |