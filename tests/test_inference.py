import numpy as np

from src.models.train_baseline import format_prediction_output


def test_format_prediction_output_shape():
    out = format_prediction_output(label=1, confidence=0.87, probabilities=np.array([0.13, 0.87]))
    assert out["predicted_label"] in [0, 1]
    assert 0.0 <= out["confidence"] <= 1.0
    assert "probabilities" in out
    assert set(out["probabilities"].keys()) == {"unreliable", "reliable"}
