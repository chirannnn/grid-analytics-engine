import { useQuery } from '@tanstack/react-query';
import { api } from '../../services/api/endpoints';
import { useState } from 'react';

export function ForecastsPage() {
  const [page, setPage] = useState(1);
  
  const { data: intervalsData, isLoading } = useQuery({
    queryKey: ['intervals', page],
    queryFn: () => api.intervals({ page, page_size: 20 }).then(res => res.data),
  });

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold mb-2">Forecast Explorer</h2>
        <p className="text-muted-foreground">Inspect forecast publications and selection logic for each delivery interval</p>
      </div>

      <div className="border rounded-lg bg-card">
        <div className="p-4 border-b">
          <h3 className="font-semibold">Delivery Intervals (Decision-Time Selected Forecasts)</h3>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-muted/50">
              <tr>
                <th className="text-left p-3 text-sm font-medium">Delivery Start</th>
                <th className="text-left p-3 text-sm font-medium">Publish Time</th>
                <th className="text-right p-3 text-sm font-medium">Forecast (MW)</th>
                <th className="text-right p-3 text-sm font-medium">Actual (MW)</th>
                <th className="text-right p-3 text-sm font-medium">Error (MW)</th>
                <th className="text-right p-3 text-sm font-medium">Lead (h)</th>
                <th className="text-center p-3 text-sm font-medium">Status</th>
              </tr>
            </thead>
            <tbody>
              {isLoading ? (
                <tr>
                  <td colSpan={7} className="p-4 text-center text-muted-foreground">Loading...</td>
                </tr>
              ) : intervalsData?.intervals?.length > 0 ? (
                intervalsData.intervals.map((interval: any, idx: number) => (
                  <tr key={idx} className="border-t hover:bg-muted/50">
                    <td className="p-3 text-sm">{new Date(interval.delivery_start).toLocaleString('en-GB')}</td>
                    <td className="p-3 text-sm">{interval.selected_forecast ? new Date(interval.selected_forecast.publish_time).toLocaleString('en-GB') : 'N/A'}</td>
                    <td className="p-3 text-sm text-right">{interval.selected_forecast?.forecast_generation?.toFixed(1) || 'N/A'}</td>
                    <td className="p-3 text-sm text-right">{interval.actual_generation !== null && interval.actual_generation !== undefined ? interval.actual_generation?.toFixed(1) : 'N/A'}</td>
                    <td className="p-3 text-sm text-right">
                      {interval.selected_forecast && interval.actual_generation !== null ? 
                        (interval.selected_forecast.forecast_generation - interval.actual_generation).toFixed(1) : 'N/A'}
                    </td>
                    <td className="p-3 text-sm text-right">
                      {interval.selected_forecast?.forecast_lead_hours ? interval.selected_forecast.forecast_lead_hours.toFixed(1) : 'N/A'}
                    </td>
                    <td className="p-3 text-sm text-center">
                      <span className={`px-2 py-1 rounded text-xs ${
                        interval.selected_forecast && interval.actual_generation !== null ? 'bg-green-100 text-green-800' :
                        interval.selected_forecast ? 'bg-yellow-100 text-yellow-800' :
                        'bg-red-100 text-red-800'
                      }`}>
                        {interval.selected_forecast && interval.actual_generation !== null ? 'Complete' :
                         interval.selected_forecast ? 'Missing Actual' : 'Missing Forecast'}
                      </span>
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan={7} className="p-4 text-center text-muted-foreground">No data available</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
