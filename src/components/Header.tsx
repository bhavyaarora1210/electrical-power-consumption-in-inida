import React from 'react';
import { Zap, Activity, TrendingUp } from 'lucide-react';

const Header: React.FC = () => {
  return (
    <header className="bg-white shadow-sm border-b border-gray-100">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-gradient-to-r from-blue-600 to-cyan-600 rounded-lg">
              <Zap className="h-6 w-6 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-gray-900">
                PowerPredict India
              </h1>
              <p className="text-sm text-gray-600">
                Real-time Electricity Consumption Forecasting
              </p>
            </div>
          </div>
          
          <div className="flex items-center space-x-6">
            <div className="flex items-center space-x-2 text-green-600">
              <Activity className="h-4 w-4" />
              <span className="text-sm font-medium">Live Monitoring</span>
            </div>
            <div className="flex items-center space-x-2 text-blue-600">
              <TrendingUp className="h-4 w-4" />
              <span className="text-sm font-medium">ML Predictions</span>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;