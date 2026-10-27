# Domain & Methodology

## Business Context

Electricity procurement analysts need to decide how much to purchase from the day-ahead wholesale market based on consumer demand and expected renewable generation. For wind generation, forecast accuracy directly impacts procurement decisions and costs.

## Critical Domain Logic

### Decision-Time Forecast Selection

The key insight: we must evaluate the forecast that was *available* at decision time, not the best forecast in hindsight.

**Process:**
1. For delivery period starting at time T_delivery, decision is made at T_decision = T_delivery - 1 day at 10:00 Europe/London
2. Find all WINDFOR forecasts for this delivery period with publishTime ≤ T_decision
3. If multiple forecasts exist, select the one with latest publishTime (most recent)
4. This is the forecast the analyst would have used for procurement
5. Compare this forecast to actual FUELHH wind generation for the same delivery period

### Why This Matters

Using a later forecast (published after decision cutoff) would give unrealistically good accuracy metrics. We must simulate the information available at decision time.

### Timezone Handling

- All times in Europe/London timezone
- January 2026 is GMT (no DST)
- Implementation must handle DST transitions correctly
- Delivery periods are half-hourly

### Data Alignment

- Actuals from FUELHH: filtered by fuelType='WIND'
- Forecasts from WINDFOR: all wind forecasts
- Match on exact delivery startTime (half-hourly periods)
- Never interpolate or fill missing data

## Metrics Definitions

| Metric | Formula | Interpretation |
|--------|---------|---------------|
| MAE | mean(\|forecast - actual\|) | Average magnitude of errors. Units: MW |
| RMSE | sqrt(mean((forecast - actual)²)) | Similar to MAE but penalizes large errors more. Units: MW |
| Mean Bias Error | mean(forecast - actual) | Systematic tendency. Positive = overforecasting. Units: MW |
| Coverage | matched_intervals / expected_intervals | Data completeness |

**Error definition:** error = forecast_generation - actual_generation

**Note on MAPE:** Not used because actual wind generation can be 0 MW, making percentage errors undefined/infinite.

## Edge Cases Handled

- Missing forecasts for a delivery interval → marked unevaluable
- Missing actuals → forecast shown but error cannot be calculated
- Duplicate records → handled explicitly
- Forecasts published exactly at cutoff → included (≤)
- Delivery periods extending to Feb 1 for Jan decisions → included
- Zero actual generation → errors calculated normally (not treated as special case)

## Assumptions

1. Decision cutoff of 10:00 Europe/London day before delivery is a reasonable pilot assumption; actual gate closure may differ
2. "Latest forecast" means most recent publishTime among eligible
3. National-level wind generation (sum across all wind farms)
4. FUELHH generation field represents actual generation in MW
5. WINDFOR generation field represents forecast generation in MW
6. Half-hourly settlement periods
