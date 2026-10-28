# WindLens Demo Script

## Part 1: Product Walkthrough (5 minutes)

### Introduction (30s)
- "WindLens - Day-Ahead Forecast Intelligence for UK wind generation procurement"
- Problem: Need to know what forecast was available at decision time and its accuracy

### Overview Dashboard (2 min)
- Show latest eligible forecast card - highlight "Selected at decision time" indicator
- Point out forecast publication time vs delivery time
- Review KPIs: MAE, RMSE, Mean Bias, Coverage
- Show forecast vs actual chart and error chart

### Forecast Explorer (1m 30s)
- Navigate to Forecast Explorer
- Show table with delivery intervals
- Highlight decision-time selected forecasts
- Explain why later forecasts excluded

### Accuracy Analysis (1 min)
- Show metrics with definitions
- Horizon comparison chart
- Export functionality
- Note units (MW) and no MAPE usage

## Part 2: Technical Review (5 minutes)

### Architecture (1m 30s)
- FastAPI backend + React/TypeScript frontend
- Elexon BMRS integration (FUELHH, WINDFOR)
- Decision-time selection logic

### Critical Logic Demo (2 min)
- Show code: `backend/app/analytics/selection.py`
- Explain cutoff logic (10:00 Europe/London day before)
- Show tests passing (11/11)
- Demonstrate: forecasts after cutoff excluded, latest eligible selected

### Deployment & Testing (1m 30s)
- Show Docker setup
- Run tests
- Show API docs
- Explain deployment options (Vercel + Render)

## Recording Notes
- Keep within 10 minutes total
- Focus on decision-time logic (key differentiator)
- Show actual running application
- Don't claim deployment if not done
