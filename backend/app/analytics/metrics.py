"""Forecast accuracy metrics."""
import math
from typing import List, Dict, Any, Optional


def calculate_mae(forecast_actual_pairs: List[Dict[str, Any]]) -> float:
    """Calculate Mean Absolute Error."""
    if not forecast_actual_pairs:
        return 0.0
    total_abs_error = sum(abs(p["forecast"] - p["actual"]) for p in forecast_actual_pairs)
    return total_abs_error / len(forecast_actual_pairs)


def calculate_rmse(forecast_actual_pairs: List[Dict[str, Any]]) -> float:
    """Calculate Root Mean Squared Error."""
    if not forecast_actual_pairs:
        return 0.0
    sum_squared_error = sum((p["forecast"] - p["actual"]) ** 2 for p in forecast_actual_pairs)
    mse = sum_squared_error / len(forecast_actual_pairs)
    return math.sqrt(mse)


def calculate_bias(forecast_actual_pairs: List[Dict[str, Any]]) -> float:
    """Calculate Mean Bias Error (signed error). Positive means overforecasting."""
    if not forecast_actual_pairs:
        return 0.0
    total_error = sum(p["forecast"] - p["actual"] for p in forecast_actual_pairs)
    return total_error / len(forecast_actual_pairs)


def calculate_coverage(matched: int, expected: int) -> float:
    """Calculate forecast accuracy coverage."""
    if expected == 0:
        return 0.0
    return matched / expected


def calculate_summary_metrics(evaluated_intervals: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Calculate all summary metrics from evaluated intervals."""
    # Filter for matched pairs with actuals
    matched_pairs = []
    for interval in evaluated_intervals:
        if interval.get("forecast") is not None and interval.get("actual") is not None:
            matched_pairs.append({
                "forecast": float(interval["forecast"]),
                "actual": float(interval["actual"])
            })
    
    matched_count = len(matched_pairs)
    expected_count = len([i for i in evaluated_intervals if i.get("expected", True)])
    
    mae = calculate_mae(matched_pairs)
    rmse = calculate_rmse(matched_pairs)
    bias = calculate_bias(matched_pairs)
    coverage = calculate_coverage(matched_count, expected_count)
    
    total_forecast = sum(p["forecast"] for p in matched_pairs) if matched_pairs else 0.0
    total_actual = sum(p["actual"] for p in matched_pairs) if matched_pairs else 0.0
    
    return {
        "mae": round(mae, 3),
        "rmse": round(rmse, 3),
        "mean_bias_error": round(bias, 3),
        "coverage": round(coverage, 3),
        "matched_intervals": matched_count,
        "expected_intervals": expected_count,
        "total_forecast_generation": round(total_forecast, 3),
        "total_actual_generation": round(total_actual, 3),
        "units": "MW"
    }
