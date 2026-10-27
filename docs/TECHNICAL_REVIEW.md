# Technical Review

## Design Philosophy

This application prioritizes **correctness of domain logic** over feature breadth. The forecast selection logic is the most critical component and has been thoroughly tested.

## Component Responsibilities

### Backend
- **Elexon Client** (`app/integrations/elexon/`): HTTP communication, retries, error handling
- **Forecast Selector** (`app/analytics/selection.py`): Decision-time logic - most critical
- **Metrics Calculator** (`app/analytics/metrics.py`): Accuracy calculations
- **API Routers** (`app/main.py`): HTTP endpoints, validation
- **Schemas** (`app/schemas/`): Pydantic models for type safety

### Frontend
- **Layout**: App shell and navigation
- **Features**: Organized by domain (overview, forecasts, accuracy, methodology)
- **API Client**: Centralized HTTP communication
- **Components**: Reusable UI elements

## Key Design Decisions

1. **Backend computes all business metrics** - Frontend never recalculates critical metrics
2. **Pure functions for logic** - Selection and metrics are easily testable
3. **Timezone-aware** - All datetime operations respect Europe/London
4. **Explicit over implicit** - Missing data marked, not filled with zeros
5. **Defensive programming** - Validation, retries, error handling throughout

## Data Flow

```
Elexon API → Client (fetch) → Normalize → Cache → Selector (apply cutoff logic) → Matcher (align intervals) → Metrics → API Response → Frontend
```

## Testing Strategy

### Backend Tests (Critical)
- `test_selection.py`: Proves decision-time logic is correct
- `test_metrics.py`: Validates metric calculations

All tests use deterministic fixtures, no live API calls.

### What We Test
- Forecasts after cutoff excluded ✓
- Latest forecast before cutoff selected ✓
- Multiple publications handled correctly ✓
- Actuals don't influence selection ✓
- Metrics calculated correctly ✓
- Edge cases (missing data, zeros) handled ✓

## Failure Handling

- **API failures**: Retries with exponential backoff
- **Missing data**: Explicitly marked as missing/unevaluable
- **Invalid requests**: Pydantic validation with clear errors
- **Timeouts**: Configured timeouts on all HTTP calls
- **Cache issues**: Graceful degradation

## Security Boundaries

- Environment variables for configuration
- No hardcoded secrets
- CORS restricted
- Input validation on all endpoints
- No SQL injection risk (no SQL database)
- Dependencies tracked

## Trade-offs

| Decision | Trade-off | Rationale |
|----------|-----------|-----------|
| File-based cache | Simplicity vs scalability | Pilot scope, easy to inspect |
| No auth | Simplicity vs security | Internal demo only |
| 10:00 cutoff assumption | Accuracy vs completeness | Documented, configurable |
| No MAPE | Completeness vs correctness | Mathematically correct given zero actuals |
| Local deployment focus | Reach vs ease | Docker Compose works everywhere |

## Performance Considerations

- January 2026 data is small (~8928 half-hour intervals max)
- No need for complex optimization
- Caching prevents repeated API calls
- Pagination handled correctly

## Future Improvements (Out of Scope)

- Database integration
- Real-time updates
- Authentication
- More granular forecasts (wind farms)
- Price data integration
- Machine learning forecasts
- Alerting system
