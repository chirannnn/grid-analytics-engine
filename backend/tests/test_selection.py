"""Tests for forecast selection logic."""
from datetime import datetime, timedelta

import pytz

from app.analytics.selection import ForecastSelector


class TestForecastSelection:
    """Test critical forecast selection logic."""

    def setup_method(self):
        self.selector = ForecastSelector(cutoff_hour=10, cutoff_minute=0, timezone="Europe/London")
        self.tz = pytz.timezone("Europe/London")

    def test_decision_cutoff_is_day_before_delivery(self):
        """Decision cutoff should be on day before delivery at 10:00."""
        delivery = self.tz.localize(datetime(2026, 1, 2, 0, 0))
        cutoff = self.selector.get_decision_cutoff(delivery)
        assert cutoff.day == 1
        assert cutoff.hour == 10
        assert cutoff.minute == 0

    def test_selects_latest_forecast_before_cutoff(self):
        """Should select latest forecast published before or at cutoff."""
        delivery = self.tz.localize(datetime(2026, 1, 2, 0, 30))
        cutoff = self.selector.get_decision_cutoff(delivery)

        forecasts = [
            {"startTime": delivery.isoformat(), "publishTime": (cutoff - timedelta(hours=2)).isoformat(), "generation": 1000},
            {"startTime": delivery.isoformat(), "publishTime": (cutoff - timedelta(hours=1)).isoformat(), "generation": 1100},
            {"startTime": delivery.isoformat(), "publishTime": cutoff.isoformat(), "generation": 1200},
        ]

        selected = self.selector.select_latest_eligible_forecast(delivery, forecasts)
        assert selected is not None
        assert selected["generation"] == 1200  # Latest before/at cutoff

    def test_excludes_forecasts_published_after_cutoff(self):
        """Should NOT select forecasts published after cutoff."""
        delivery = self.tz.localize(datetime(2026, 1, 2, 0, 30))
        cutoff = self.selector.get_decision_cutoff(delivery)

        forecasts = [
            {"startTime": delivery.isoformat(), "publishTime": (cutoff - timedelta(hours=1)).isoformat(), "generation": 1100},
            {"startTime": delivery.isoformat(), "publishTime": (cutoff + timedelta(minutes=30)).isoformat(), "generation": 1500},  # After cutoff
        ]

        selected = self.selector.select_latest_eligible_forecast(delivery, forecasts)
        assert selected is not None
        assert selected["generation"] == 1100  # Only the one before cutoff

    def test_returns_none_if_no_forecasts_before_cutoff(self):
        """Should return None if no forecasts published before cutoff."""
        delivery = self.tz.localize(datetime(2026, 1, 2, 0, 30))
        cutoff = self.selector.get_decision_cutoff(delivery)

        forecasts = [
            {"startTime": delivery.isoformat(), "publishTime": (cutoff + timedelta(hours=1)).isoformat(), "generation": 1100},
        ]

        selected = self.selector.select_latest_eligible_forecast(delivery, forecasts)
        assert selected is None

    def test_never_uses_actual_to_select_forecast(self):
        """Selection must not depend on actual generation."""
        delivery = self.tz.localize(datetime(2026, 1, 2, 0, 30))
        cutoff = self.selector.get_decision_cutoff(delivery)

        forecasts = [
            {"startTime": delivery.isoformat(), "publishTime": (cutoff - timedelta(hours=2)).isoformat(), "generation": 1000},
        ]

        # Actual not passed to selection - this is correct
        selected = self.selector.select_latest_eligible_forecast(delivery, forecasts)
        assert selected["generation"] == 1000
