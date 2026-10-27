import { apiClient } from './client';

export const api = {
  health: () => apiClient.get('/api/health'),
  ready: () => apiClient.get('/api/health/ready'),
  metadata: () => apiClient.get('/api/metadata'),
  latestForecast: () => apiClient.get('/api/forecasts/latest'),
  intervals: (params?: any) => apiClient.get('/api/forecasts/intervals', { params }),
  history: (params?: any) => apiClient.get('/api/forecasts/history', { params }),
  analysisSummary: (params?: any) => apiClient.get('/api/analysis/summary', { params }),
  analysisTimeseries: (params?: any) => apiClient.get('/api/analysis/timeseries', { params }),
  analysisErrors: (params?: any) => apiClient.get('/api/analysis/errors', { params }),
  analysisHorizons: (params?: any) => apiClient.get('/api/analysis/horizons', { params }),
  refreshData: () => apiClient.post('/api/data/refresh'),
};
