import { useQuery } from '@tanstack/react-query';
import { api } from '../../services/api/endpoints';
import { Database, Clock, Target, Calculator } from 'lucide-react';

export function MethodologyPage() {
  const { data: metadata } = useQuery({
    queryKey: ['metadata'],
    queryFn: () => api.metadata().then(res => res.data),
  });

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold mb-2">Data & Methodology</h2>
        <p className="text-muted-foreground">Elexon data sources, forecast selection logic, and metrics</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="border rounded-lg p-4 bg-card">
          <h3 className="text-lg font-semibold mb-3 flex items-center">
            <Database className="h-5 w-5 mr-2" />
            Data Sources
          </h3>
          <div className="space-y-3 text-sm">
            <div>
              <p className="font-medium">Actual Generation - FUELHH</p>
              <p className="text-muted-foreground">Records with fuelType='WIND', generation in MW</p>
              <a href="https://bmrs.elexon.co.uk/api-documentation/endpoint/datasets/FUELHH/stream" target="_blank" rel="noopener noreferrer" className="text-primary hover:underline text-xs">
                API Documentation
              </a>
            </div>
            <div>
              <p className="font-medium">Forecast Generation - WINDFOR</p>
              <p className="text-muted-foreground">startTime (delivery), publishTime (publication), generation in MW</p>
              <a href="https://bmrs.elexon.co.uk/api-documentation/endpoint/datasets/WINDFOR/stream" target="_blank" rel="noopener noreferrer" className="text-primary hover:underline text-xs">
                API Documentation
              </a>
            </div>
          </div>
        </div>

        <div className="border rounded-lg p-4 bg-card">
          <h3 className="text-lg font-semibold mb-3 flex items-center">
            <Clock className="h-5 w-5 mr-2" />
            Decision-Time Logic
          </h3>
          <div className="space-y-2 text-sm">
            <p><strong>Evaluation Period:</strong> {metadata?.evaluation_period || 'January 2026'}</p>
            <p><strong>Decision Cutoff:</strong> {metadata?.decision_cutoff || '10:00 Europe/London day before delivery'}</p>
            <p><strong>Timezone:</strong> {metadata?.timezone || 'Europe/London'}</p>
            <p className="text-muted-foreground mt-2">For each delivery period D, we evaluate forecasts published at or before 10:00 on D-1. We select the latest (most recent) eligible forecast. Forecasts published after cutoff are excluded.</p>
          </div>
        </div>

        <div className="border rounded-lg p-4 bg-card">
          <h3 className="text-lg font-semibold mb-3 flex items-center">
            <Target className="h-5 w-5 mr-2" />
            Selection Rules
          </h3>
          <ul className="space-y-1 text-sm text-muted-foreground">
            <li>• Match forecasts to actuals by exact same delivery interval (startTime)</li>
            <li>• Filter forecasts where publishTime ≤ decision cutoff</li>
            <li>• Select latest eligible forecast (max publishTime)</li>
            <li>• Never use actual generation to select forecast</li>
            <li>• Never fill missing data with zero</li>
            <li>• Error = forecast_generation - actual_generation</li>
          </ul>
        </div>

        <div className="border rounded-lg p-4 bg-card">
          <h3 className="text-lg font-semibold mb-3 flex items-center">
            <Calculator className="h-5 w-5 mr-2" />
            Metrics
          </h3>
          <ul className="space-y-1 text-sm text-muted-foreground">
            <li>• <strong>MAE:</strong> Mean Absolute Error = mean(|forecast - actual|)</li>
            <li>• <strong>RMSE:</strong> Root Mean Square Error = sqrt(mean((forecast - actual)²))</li>
            <li>• <strong>Bias:</strong> Mean Bias Error = mean(forecast - actual)</li>
            <li>• <strong>Coverage:</strong> matched_intervals / expected_intervals</li>
            <li>• <strong>Units:</strong> MW (power)</li>
            <li>• <strong>Note:</strong> MAPE not used (actuals can be zero)</li>
          </ul>
        </div>
      </div>

      <div className="border rounded-lg p-4 bg-card">
        <h3 className="text-lg font-semibold mb-3">Assumptions & Limitations</h3>
        <ul className="space-y-1 text-sm text-muted-foreground">
          {metadata?.assumptions?.map((a: string, idx: number) => (
            <li key={idx}>• {a}</li>
          ))}
        </ul>
      </div>
    </div>
  );
}
