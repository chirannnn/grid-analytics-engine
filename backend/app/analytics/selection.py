"""Forecast selection logic - critical domain logic."""
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import pytz


class ForecastSelector:
    """Implements decision-time forecast selection logic."""
    
    def __init__(self, cutoff_hour: int = 10, cutoff_minute: int = 0, timezone: str = "Europe/London"):
        self.cutoff_hour = cutoff_hour
        self.cutoff_minute = cutoff_minute
        self.tz = pytz.timezone(timezone)
    
    def get_decision_cutoff(self, delivery_date: datetime) -> datetime:
        """
        Get decision cutoff for a delivery period.
        For delivery on date D, decision is made at cutoff on D-1.
        Default: 10:00 Europe/London on day before delivery.
        """
        # Ensure timezone aware
        if delivery_date.tzinfo is None:
            delivery_date = self.tz.localize(delivery_date)
        else:
            delivery_date = delivery_date.astimezone(self.tz)
        
        # Decision cutoff is on day before delivery
        decision_day = delivery_date - timedelta(days=1)
        cutoff = decision_day.replace(
            hour=self.cutoff_hour,
            minute=self.cutoff_minute,
            second=0,
            microsecond=0
        )
        return cutoff
    
    def select_latest_eligible_forecast(
        self, 
        delivery_start: datetime, 
        forecasts: List[Dict[str, Any]]
    ) -> Optional[Dict[str, Any]]:
        """
        Select the latest forecast published at or before decision cutoff.
        NEVER select forecast published after cutoff.
        NEVER use actual generation to select forecast.
        """
        cutoff = self.get_decision_cutoff(delivery_start)
        
        # Filter forecasts published at or before cutoff
        eligible = []
        for f in forecasts:
            publish_time = f.get("publishTime") or f.get("publish_time")
            if publish_time is None:
                continue
            
            # Ensure timezone aware
            if isinstance(publish_time, str):
                # Parse if string
                try:
                    from dateutil import parser
                    publish_time = parser.parse(publish_time)
                except:
                    continue
            
            if publish_time.tzinfo is None:
                publish_time = self.tz.localize(publish_time)
            else:
                publish_time = publish_time.astimezone(self.tz)
            
            if publish_time <= cutoff:
                eligible.append({**f, "publish_time_parsed": publish_time})
        
        if not eligible:
            return None
        
        # Select latest (most recent publish time)
        latest = max(eligible, key=lambda x: x["publish_time_parsed"])
        return latest
    
    def evaluate_intervals(
        self,
        forecasts: List[Dict[str, Any]],
        actuals: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Evaluate all delivery intervals for January 2026 decision window.
        Match actuals and forecasts by exact same delivery interval.
        """
        # Build actuals lookup by delivery start
        actuals_lookup = {}
        for a in actuals:
            start = a.get("startTime") or a.get("start_time") or a.get("delivery_start")
            if start:
                if isinstance(start, str):
                    from dateutil import parser
                    start = parser.parse(start)
                key = start.isoformat()
                actuals_lookup[key] = float(a.get("generation") or a.get("actual_generation") or 0)
        
        # Group forecasts by delivery start
        forecasts_by_delivery = {}
        for f in forecasts:
            start = f.get("startTime") or f.get("start_time") or f.get("delivery_start")
            if start:
                if isinstance(start, str):
                    from dateutil import parser
                    start = parser.parse(start)
                key = start.isoformat()
                if key not in forecasts_by_delivery:
                    forecasts_by_delivery[key] = []
                forecasts_by_delivery[key].append(f)
        
        evaluated = []
        for delivery_key, delivery_forecasts in forecasts_by_delivery.items():
            delivery_start = delivery_forecasts[0].get("startTime") or delivery_forecasts[0].get("start_time")
            if isinstance(delivery_start, str):
                from dateutil import parser
                delivery_start = parser.parse(delivery_start)
            
            # Select latest eligible forecast
            selected = self.select_latest_eligible_forecast(delivery_start, delivery_forecasts)
            
            if selected is None:
                evaluated.append({
                    "delivery_start": delivery_start.isoformat(),
                    "forecast": None,
                    "actual": actuals_lookup.get(delivery_key),
                    "publish_time": None,
                    "forecast_lead_hours": None,
                    "error": None,
                    "abs_error": None,
                    "status": "missing_forecast"
                })
                continue
            
            forecast_gen = float(selected.get("generation") or selected.get("forecast_generation") or 0)
            actual_gen = actuals_lookup.get(delivery_key)
            publish_time = selected.get("publishTime") or selected.get("publish_time")
            
            if isinstance(publish_time, str):
                from dateutil import parser
                publish_time = parser.parse(publish_time)
            
            # Calculate lead time
            if delivery_start.tzinfo and publish_time.tzinfo:
                lead_delta = delivery_start - publish_time.astimezone(delivery_start.tzinfo)
                lead_hours = lead_delta.total_seconds() / 3600
            else:
                lead_hours = None
            
            # Calculate error only if actual exists
            error = None
            abs_error = None
            if actual_gen is not None:
                error = forecast_gen - actual_gen  # forecast - actual
                abs_error = abs(error)
            
            evaluated.append({
                "delivery_start": delivery_start.isoformat(),
                "forecast": forecast_gen,
                "actual": actual_gen,
                "publish_time": publish_time.isoformat() if publish_time else None,
                "forecast_lead_hours": lead_hours,
                "error": error,
                "abs_error": abs_error,
                "status": "ok" if actual_gen is not None else "missing_actual"
            })
        
        return evaluated
