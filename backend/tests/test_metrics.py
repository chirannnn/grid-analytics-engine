"""Tests for metrics calculation."""
from app.analytics.metrics import calculate_bias, calculate_coverage, calculate_mae, calculate_rmse


class TestMetrics:
    """Test accuracy metrics calculations."""

    def test_mae_calculation(self):
        """Test MAE calculation."""
        pairs = [
            {"forecast": 1000, "actual": 900},  # error +100
            {"forecast": 950, "actual": 1000}, # error -50
            {"forecast": 1100, "actual": 1050}, # error +50
        ]
        mae = calculate_mae(pairs)
        assert abs(mae - 200/3) < 0.001  # (100+50+50)/3

    def test_rmse_calculation(self):
        """Test RMSE calculation."""
        pairs = [
            {"forecast": 100, "actual": 90},
            {"forecast": 110, "actual": 100},
        ]
        rmse = calculate_rmse(pairs)
        assert rmse == 10.0  # sqrt((10^2 + 10^2)/2)

    def test_bias_positive_means_overforecast(self):
        """Test bias calculation - positive means overforecasting."""
        pairs = [
            {"forecast": 1100, "actual": 1000},
            {"forecast": 1050, "actual": 1000},
        ]
        bias = calculate_bias(pairs)
        assert bias == 75.0  # overforecasting

    def test_bias_negative_means_underforecast(self):
        """Test bias calculation - negative means underforecasting."""
        pairs = [
            {"forecast": 900, "actual": 1000},
            {"forecast": 950, "actual": 1000},
        ]
        bias = calculate_bias(pairs)
        assert bias == -75.0

    def test_coverage_calculation(self):
        """Test coverage calculation."""
        assert calculate_coverage(10, 20) == 0.5
        assert calculate_coverage(0, 10) == 0.0
        assert calculate_coverage(5, 0) == 0.0

    def test_empty_pairs(self):
        """Test with empty pairs."""
        assert calculate_mae([]) == 0.0
        assert calculate_rmse([]) == 0.0
        assert calculate_bias([]) == 0.0
