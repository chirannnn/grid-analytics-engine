import { useQuery } from '@tanstack/react-query';
import { api } from '../../services/api/endpoints';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Download } from 'lucide-react';

export function AccuracyPage() {
  const { data: summaryData } = useQuery({
    queryKey: ['analysis-summary'],
    queryFn: () => api.analysisSummary().then(res => res.data),
  });

  const { data: horizonsData } = useQuery({
    queryKey: ['analysis-horizons'],
    queryFn: () => api.analysisHorizons().then(res => res.data),
  });

  const horizonsChartData = horizonsData?.horizons?.map((h: any) => ({
    horizon: h.horizon_label,
    MAE: h.mae,
    RMSE: h.rmse,
    Bias: h.mean_bias_error,
  })) || [];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold mb-2">Accuracy Analysis</h2>
          <p className="text-muted-foreground">Forecast accuracy metrics for decision-time selected forecasts</p>
        </div>
        <button className="flex items-center space-x-2 px-4 py-2 border rounded-lg hover:bg-muted">
          <Download className="h-4 w-4" />
          <span>Export CSV</span>
        </button>
      </div>

      {/* KPI Cards with Definitions */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="border rounded-lg p-4 bg-card">
          <div>
            <p className="text-sm text-muted-foreground">MAE</p>
            <p className="text-2xl font-bold">{summaryData?.mae?.toFixed(2)} MW</p>
            <p className="text-xs text-muted-foreground mt-1">Mean Absolute Error</p>
          </div>
        </div>
        <div className="border rounded-lg p-4 bg-card">
          <div>
            <p className="text-sm text-muted-foreground">RMSE</p>
            <p className="text-2xl font-bold">{summaryData?.rmse?.toFixed(2)} MW</p>
            <p className="text-xs text-muted-foreground mt-1">Root Mean Square Error</p>
          </div>
        </div>
        <div className="border rounded-lg p-4 bg-card">
          <div>
            <p className="text-sm text-muted-foreground">Mean Bias Error</p>
            <p className="text-2xl font-bold">{summaryData?.mean_bias_error?.toFixed(2)} MW</p>
            <p className="text-xs text-muted-foreground mt-1">Forecast - Actual (positive = overforecast)</p>
          </div>
        </div>
        <div className="border rounded-lg p-4 bg-card">
          <div>
            <p className="text-sm text-muted-foreground">Coverage</p>
            <p className="text-2xl font-bold">{((summaryData?.coverage || 0) * 100).toFixed(1)}%</p>
            <p className="text-xs text-muted-foreground mt-1">{summaryData?.matched_intervals}/{summaryData?.expected_intervals} matched</p>
          </div>
        </div>
      </div>

      {/* Horizon Comparison */}
      <div className="border rounded-lg p-4 bg-card">
        <h3 className="text-lg font-semibold mb-4">Forecast Accuracy by Lead Time Horizon</h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={horizonsChartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="horizon" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="MAE" fill="#3b82f6" />
            <Bar dataKey="RMSE" fill="#ef4444" />
            <Bar dataKey="Bias" fill="#f59e0b" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="border rounded-lg p-4 bg-card">
        <h3 className="text-lg font-semibold mb-2">Metric Definitions</h3>
        <div className="space-y-2 text-sm text-muted-foreground">
          <p><strong>MAE:</strong> Mean of |forecast - actual|. Lower is better.</p>
          <p><strong>RMSE:</strong> Square root of mean of (forecast - actual)². Penalizes larger errors more heavily.</p>
          <p><strong>Mean Bias Error:</strong> Mean of (forecast - actual). Positive = systematic overforecasting, negative = underforecasting.</p>
          <p><strong>Coverage:</strong> Proportion of intervals with both forecast and actual data.</p>
          <p className="text-xs italic">Note: MAPE not used as primary metric because actual wind generation can be zero or near zero.</p>
        </div>
      </div>
    </div>
  );
}
