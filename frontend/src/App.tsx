import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Layout } from './components/layout/Layout';
import { OverviewPage } from './features/overview/OverviewPage';
import { ForecastsPage } from './features/forecasts/ForecastsPage';
import { AccuracyPage } from './features/accuracy/AccuracyPage';
import { MethodologyPage } from './features/methodology/MethodologyPage';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Layout />}>
            <Route index element={<OverviewPage />} />
            <Route path="forecasts" element={<ForecastsPage />} />
            <Route path="accuracy" element={<AccuracyPage />} />
            <Route path="methodology" element={<MethodologyPage />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App;
