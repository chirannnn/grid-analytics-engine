import { Link, Outlet, useLocation } from 'react-router-dom';
import { Wind, BarChart3, Search, BookOpen, Activity } from 'lucide-react';

const navigation = [
  { name: 'Overview', href: '/', icon: BarChart3 },
  { name: 'Forecast Explorer', href: '/forecasts', icon: Search },
  { name: 'Accuracy Analysis', href: '/accuracy', icon: Activity },
  { name: 'Data & Methodology', href: '/methodology', icon: BookOpen },
];

export function Layout() {
  const location = useLocation();

  return (
    <div className="min-h-screen bg-background">
      <header className="border-b">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <Wind className="h-8 w-8 text-primary" />
              <div>
                <h1 className="text-xl font-bold">WindLens</h1>
                <p className="text-xs text-muted-foreground">Day-Ahead Forecast Intelligence</p>
              </div>
            </div>
            <div className="flex items-center space-x-4 text-sm text-muted-foreground">
              <span className="px-2 py-1 bg-muted rounded">Evaluation Period: Jan 2026</span>
            </div>
          </div>
        </div>
      </header>

      <nav className="border-b">
        <div className="container mx-auto px-4">
          <div className="flex space-x-6">
            {navigation.map((item) => {
              const Icon = item.icon;
              const isActive = location.pathname === item.href;
              return (
                <Link
                  key={item.name}
                  to={item.href}
                  className={`flex items-center space-x-2 py-3 px-1 border-b-2 transition-colors ${
                    isActive
                      ? 'border-primary text-primary'
                      : 'border-transparent text-muted-foreground hover:text-foreground'
                  }`}
                >
                  <Icon className="h-4 w-4" />
                  <span>{item.name}</span>
                </Link>
              );
            })}
          </div>
        </div>
      </nav>

      <main className="container mx-auto px-4 py-6">
        <Outlet />
      </main>

      <footer className="border-t mt-12">
        <div className="container mx-auto px-4 py-4 text-center text-sm text-muted-foreground">
          <p>WindLens — UK Wind Forecast Intelligence Platform (Pilot)</p>
        </div>
      </footer>
    </div>
  );
}
