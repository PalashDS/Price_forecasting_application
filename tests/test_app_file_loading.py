import pytest
import os
from tensorflow.keras.models import load_model
import numpy as np

def test_model_file_exists():
    assert os.path.exists("updated_lstm_model.h5"), "Model file is missing."

def test_model_loading():
    try:
        model = load_model("updated_lstm_model.h5")
        assert model is not None, "Model loading failed."
    except Exception as e:
        pytest.fail(f"Model loading raised an exception: {e}")

def test_data_file_exists():
    assert os.path.exists("data_scaled.npy"), "Data file is missing."

def test_data_loading():
    try:
        data_scaled = np.load("data_scaled.npy")
        assert data_scaled is not None, "Data loading failed."
        assert len(data_scaled.shape) > 0, "Data file is empty or corrupted."
    except Exception as e:
        pytest.fail(f"Data loading raised an exception: {e}")
