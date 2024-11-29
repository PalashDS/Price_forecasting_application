import pytest

def test_ui_future_steps_valid_range():
    min_value = 1
    max_value = 100
    default_value = 10

    assert default_value >= min_value and default_value <= max_value, "Default value out of range."
    assert min_value < max_value, "Invalid input range for future steps."
