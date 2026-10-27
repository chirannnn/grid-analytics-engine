# WindLens Demo Script (10 Minutes Total)

## Part 1: Customer-Facing Product Demonstration (5 minutes)

### Introduction (30 seconds)
- **Product name:** WindLens - Day-Ahead Forecast Intelligence
- **Audience:** Electricity procurement analysts
- **Value proposition:** Know what forecast was available at decision time and how accurate it was

### Overview Dashboard (2 minutes)
1. **Show the dashboard** - Highlight clean, professional energy analytics UI
2. **Latest Eligible Forecast card** - Emphasize "Selected at decision time ✓" indicator
   - Point out delivery time, publication time, forecast vs actual
   - Show forecast was selected using cutoff logic
3. **KPI cards** - MAE, RMSE, Mean Bias, Coverage
   - Explain units are MW
   - Note positive bias means overforecasting
4. **Charts** - Forecast vs Actual time series, Error over time
   - Show zero-reference on error chart

### Forecast Explorer (1 minute 30 seconds)
1. **Navigate to Forecast Explorer**
2. **Show table** - Delivery intervals with selected forecast details
3. **Highlight key columns:** publish time, forecast, actual, error, lead time
4. **Point out status indicators:** Complete, Missing Actual, Missing Forecast
5. **Emphasize:** This shows the forecast that WOULD have been used at decision time

### Accuracy Analysis (1 minute)
1. **Navigate to Accuracy Analysis**
2. **Show KPI definitions** - transparency in methodology
3. **Horizon comparison chart** - accuracy by lead time
4. **Mention export functionality** - CSV download for further analysis
5. **Note:** MAPE not used because actuals can be zero

## Part 2: Technical Review & Knowledge Transfer (5 minutes)

### Architecture Overview (1 minute 30 seconds)
1. **Show README architecture diagram**
2. **Tech stack:** React/TypeScript frontend, FastAPI/Python backend
3. **Data flow:** Elexon API → normalization → selection logic → metrics → API → UI
4. **Docker Compose** for easy local deployment

### Critical Domain Logic (2 minutes)
1. **Open Domain & Methodology doc**
2. **Demonstrate the key logic:**
   - Decision cutoff: 10:00 Europe/London day before delivery
   - Select forecasts with publishTime ≤ cutoff
   - Choose LATEST eligible forecast
   - Never use actuals for selection
   - Never use forecasts published after cutoff
3. **Show backend tests** - `test_selection.py` proves these rules
   - Test excludes forecasts after cutoff
   - Test selects latest before cutoff
   - Test doesn't use actuals for selection

### Implementation Highlights (1 minute 30 seconds)
1. **Code structure** - Clean separation of concerns
2. **Type safety** - Pydantic schemas, TypeScript types
3. **Testing** - Unit tests for critical logic
4. **Error handling** - Missing data handled honestly (not filled with zeros)
5. **Documentation** - Comprehensive docs, assumptions recorded
6. **Git history** - Coherent commits
7. **Show how to run:** `docker compose up --build`

### Q&A Preparation
- **"Why 10:00 cutoff?"** - Pilot assumption, documented, configurable
- **"Why no MAPE?"** - Division by zero when actual is 0
- **"How do you ensure decision-time logic?"** - Unit tests enforce it, logic is explicit
- **"Can this scale?"** - Pilot design, would need DB, auth, etc for production

## Recording Checklist

- [ ] Screen recording software ready
- [ ] Application running (local or deployed)
- [ ] All pages load correctly
- [ ] Data visible on dashboards
- [ ] Tests can be shown
- [ ] Code structure visible
- [ ] Documentation accessible
- [ ] Audio clear
- [ ] Within 10 minutes total
- [ ] Part 1 under 5 minutes, Part 2 under 5 minutes

## Features to Demonstrate

**Must show:**
- Decision-time selection indicator
- Forecast vs actual comparison
- Metrics with definitions
- Forecast Explorer table
- Unit tests for selection logic
- Methodology documentation

**Nice to show:**
- Docker Compose startup
- API documentation (/docs)
- Git commit history
- Error handling for missing data
