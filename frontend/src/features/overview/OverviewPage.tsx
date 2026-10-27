import { useQuery } from '@tanstack/react-query';
import { api } from '../../services/api/endpoints';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, LineChart, Line } from 'recharts';
import { Wind, TrendingUp, TrendingDown, Activity } from 'lucide-react';

export function OverviewPage() {
  const { data: latestData, isLoading: latestLoading } = useQuery({
    queryKey: ['latest-forecast'],
    queryFn: () => api.latestForecast().then(res => res.data),
  });

  const { data: summaryData } = useQuery({
    queryKey: ['analysis-summary'],
    queryFn: () => api.analysisSummary().then(res => res.data),
  });

  const { data: timeseriesData } = useQuery({
    queryKey: ['analysis-timeseries'],
    queryFn: () => api.analysisTimeseries().then(res => res.data),
  });

  if (latestLoading) {
    return (
      <div className="space-y-6">
        <div className="h-32 bg-muted animate-pulse rounded" />
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          {[1,2,3,4].map(i => (
            <div key={i} className="h-24 bg-muted animate-pulse rounded" />
          ))}
        </div>
      </div>
    );
  }

  const chartData = timeseriesData?.data?.slice(0, 48).map((d: any) => ({
    time: new Date(d.delivery_start).toLocaleString('en-GB', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' }),
    forecast: d.forecast_generation,
    actual: d.actual_generation,
  })) || [];

  const errorData = timeseriesData?.data?.slice(0, 48).filter((d: any) => d.error !== null).map((d: any) => ({
    time: new Date(d.delivery_start).toLocaleString('en-GB', { month: 'short', day: 'numeric', hour: '2-digit' }),
    error: d.error,
  })) || [];

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold mb-2">Overview Dashboard</h2>
        <p className="text-muted-foreground">Day-ahead wind forecast intelligence for January 2026 procurement decisions</p>
      </div>

      {/* Latest Forecast Card */}
      <div className="border rounded-lg p-6 bg-card">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold flex items-center">
            <Wind className="h-5 w-5 mr-2 text-primary" />
            Latest Eligible Forecast (Decision-Time)
          </h3>
          <span className="text-xs px-2 py-1 bg-green-100 text-green-800 rounded">
            Selected at decision time ✓
          </span>
        </div>
        {latestData ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <div>
              <p className="text-sm text-muted-foreground">Delivery Start</p>
              <p className="font-medium">{new Date(latestData.delivery_start).toLocaleString('en-GB')}</p>
            </div>
            <div>
              <p className="text-sm text-muted-foreground">Forecast Published</p>
              <p className="font-medium">{new Date(latestData.publish_time).toLocaleString('en-GB')}</p>
            </div>
            <div>
              <p className="text-sm text-muted-foreground">Forecast Generation</p>
              <p className="text-2xl font-bold">{latestData.forecast_generation?.toFixed(1)} MW</p>
            </div>
            <div>
              <p className="text-sm text-muted-foreground">Actual Generation</p>
              <p className="text-2xl font-bold">{latestData.actual_generation !== null ? `${latestData.actual_generation?.toFixed(1)} MW` : 'N/A'}</p>
            </div>
          </div>
        ) : (
          <p className="text-muted-foreground">No data available. Use Data & Methodology to refresh.</p>
        )}
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="border rounded-lg p-4 bg-card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-muted-foreground">MAE</p>
              <p className="text-2xl font-bold">{summaryData?.mae?.toFixed(1) || '0.0'}</p>
              <p className="text-xs text-muted-foreground">MW</p>
            </div>
            <Activity className="h-8 w-8 text-muted-foreground" />
          </div>
        </div>
        <div className="border rounded-lg p-4 bg-card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-muted-foreground">RMSE</p>
              <p className="text-2xl font-bold">{summaryData?.rmse?.toFixed(1) || '0.0'}</p>
              <p className="text-xs text-muted-foreground">MW</p>
            </div>
            <TrendingUp className="h-8 w-8 text-muted-foreground" />
          </div>
        </div>
        <div className="border rounded-lg p-4 bg-card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-muted-foreground">Mean Bias</p>
              <p className={`text-2xl font-bold ${(summaryData?.mean_bias_error || 0) > 0 ? 'text-orange-600' : (summaryData?.mean_bias_error || 0) < 0 ? 'text-blue-600' : ''}`}>
                {(summaryData?.mean_bias_error || 0) > 0 ? '+' : ''}{summaryData?.mean_bias_error?.toFixed(1) || '0.0'}
              </p>
              <p className="text-xs text-muted-foreground">MW</p>
            </div>
            <TrendingDown className="h-8 w-8 text-muted-foreground" />
          </div>
        </div>
        <div className="border rounded-lg p-4 bg-card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-muted-foreground">Coverage</p>
              <p className="text-2xl font-bold">{((summaryData?.coverage || 0) * 100).toFixed(1)}%</p>
              <p className="text-xs text-muted-foreground">{summaryData?.matched_intervals || 0}/{summaryData?.expected_intervals || 0} intervals</p>
            </div>
            <Activity className="h-8 w-8 text-muted-foreground" />
          </div>
        </div>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="border rounded-lg p-4 bg-card">
          <h3 className="text-lg font-semibold mb-4">Forecast vs Actual (First 48 Intervals)</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="time" tick={{ fontSize: 10 }} />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="forecast" stroke="#3b82f6" name="Forecast (MW)" strokeWidth={2} />
              <Line type="monotone" dataKey="actual" stroke="#10b981" name="Actual (MW)" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </div>
        <div className="border rounded-lg p-4 bg-card">
          <h3 className="text-lg font-semibold mb-4">Error Over Time (Forecast - Actual)</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={errorData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="time" tick={{ fontSize: 10 }} />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="error" fill="#f59e0b" name="Error (MW)" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
