# Architecture

## System Overview

WindLens is a three-tier web application consisting of a React frontend, FastAPI backend, and integration with Elexon BMRS APIs.

## Components

### Frontend (React + TypeScript + Vite)
- **App Shell**: Layout with navigation, branding, evaluation period indicator
- **Overview Dashboard**: Key metrics and time series visualizations
- **Forecast Explorer**: Detailed inspection of forecast publications
- **Accuracy Analysis**: Metrics, charts, and exports
- **Methodology Page**: Documentation of data sources and logic

### Backend (FastAPI)
- **API Layer**: RESTful endpoints with Pydantic validation
- **Integration Layer**: Elexon API client with retries and pagination
- **Analytics Layer**: Forecast selection and metrics calculation
- **Cache Layer**: Local file-based caching of normalized data

### Data Flow

1. User triggers data refresh via API
2. Backend fetches FUELHH (actuals) and WINDFOR (forecasts) from Elexon
3. Data normalized and cached locally
4. Forecast selection logic applied per delivery interval
5. Metrics calculated on matched pairs
6. API serves processed data to frontend
7. Frontend visualizes results

## Key Design Decisions

- **Separation of concerns**: Business logic in backend, presentation in frontend
- **Type safety**: TypeScript frontend, Pydantic backend
- **Testability**: Pure functions for selection and metrics logic
- **Resilience**: Retries, error handling, caching
- **Transparency**: All assumptions documented

## Security

- No secrets committed to repo
- CORS restricted to configured origins
- Environment-based configuration
- No authentication in pilot (internal use)

## Scalability Notes

This is a pilot application. For production:
- Add authentication/authorization
- Use proper database (Postgres/TimescaleDB)
- Implement job queue for data refresh
- Add monitoring and logging
- Use CDN for frontend
- Implement rate limiting
