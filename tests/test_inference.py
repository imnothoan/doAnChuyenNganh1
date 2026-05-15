import numpy as np

from src.models.inference import UNRELIABLE_LABEL, predict_probabilities
from src.models.train_baseline import format_prediction_output


def test_format_prediction_output_shape():
    out = format_prediction_output(label=1, confidence=0.87, probabilities=np.array([0.13, 0.87]))
    assert out["predicted_label"] in [0, 1]
    assert out["label_name"] == "unreliable"
    assert 0.0 <= out["confidence"] <= 1.0
    assert "probabilities" in out
    assert set(out["probabilities"].keys()) == {"unreliable", "reliable"}
    assert out["probabilities"]["unreliable"] == 0.87


def test_predict_probabilities_respects_model_classes_order():
    class FakeModel:
        classes_ = np.array([0, 1])

        def predict_proba(self, texts):
            return np.array([[0.2, 0.8] for _ in texts])

    probs = predict_probabilities(FakeModel(), ["abc"])[0]

    assert probs["unreliable"] == 0.8
    assert probs["reliable"] == 0.2
    assert UNRELIABLE_LABEL == 1
