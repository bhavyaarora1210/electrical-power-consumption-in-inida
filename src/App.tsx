import React from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import Dashboard from './components/Dashboard';

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
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-cyan-50">
        <Dashboard />
      </div>
    </QueryClientProvider>
  );
}

export default App;