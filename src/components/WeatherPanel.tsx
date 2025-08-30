import React from 'react';
import { Thermometer, Droplets, Wind, CloudRain, RefreshCw } from 'lucide-react';

interface WeatherPanelProps {
  weatherData: any;
  onRefresh: () => void;
  isLoading: boolean;
}

const WeatherPanel: React.FC<WeatherPanelProps> = ({ weatherData, onRefresh, isLoading }) => {
  const weatherItems = [
    {
      label: 'Temperature',
      value: `${weatherData?.temperature?.toFixed(1)}°C`,
      icon: Thermometer,
      color: 'text-red-500',
      bgColor: 'bg-red-50',
    },
    {
      label: 'Humidity',
      value: `${weatherData?.humidity?.toFixed(0)}%`,
      icon: Droplets,
      color: 'text-blue-500',
      bgColor: 'bg-blue-50',
    },
    {
      label: 'Wind Speed',
      value: `${weatherData?.wind_speed?.toFixed(1)} km/h`,
      icon: Wind,
      color: 'text-gray-500',
      bgColor: 'bg-gray-50',
    },
    {
      label: 'Rainfall',
      value: `${weatherData?.rainfall?.toFixed(1)} mm`,
      icon: CloudRain,
      color: 'text-cyan-500',
      bgColor: 'bg-cyan-50',
    },
  ];

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-gray-900">Weather Conditions</h3>
        <button
          onClick={onRefresh}
          disabled={isLoading}
          className="p-2 text-gray-500 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors disabled:opacity-50"
        >
          <RefreshCw className={`h-4 w-4 ${isLoading ? 'animate-spin' : ''}`} />
        </button>
      </div>

      <div className="space-y-3">
        {weatherItems.map((item, index) => {
          const Icon = item.icon;
          return (
            <div key={index} className="flex items-center space-x-3 p-3 rounded-lg hover:bg-gray-50 transition-colors">
              <div className={`p-2 rounded-lg ${item.bgColor}`}>
                <Icon className={`h-4 w-4 ${item.color}`} />
              </div>
              <div className="flex-1">
                <p className="text-sm text-gray-600">{item.label}</p>
                <p className="font-semibold text-gray-900">{item.value}</p>
              </div>
            </div>
          );
        })}
      </div>

      {weatherData?.location && (
        <div className="mt-4 pt-4 border-t border-gray-100">
          <p className="text-xs text-gray-500">Location: {weatherData.location}</p>
          {weatherData.error && (
            <p className="text-xs text-amber-600 mt-1">⚠️ {weatherData.error}</p>
          )}
        </div>
      )}
    </div>
  );
};

export default WeatherPanel;