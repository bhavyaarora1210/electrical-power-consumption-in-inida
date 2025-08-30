import React from 'react';
import { Zap, TrendingUp, Clock, Target, Download } from 'lucide-react';
import { format } from 'date-fns';

interface PredictionData {
  state: string;
  district: string;
  current_prediction: number;
  confidence_score: number;
  weather_data: any;
  parameters: any;
  predictions_24h: any[];
  timestamp: string;
}

interface PredictionCardsProps {
  predictionData: PredictionData;
  isLoading: boolean;
}

const PredictionCards: React.FC<PredictionCardsProps> = ({ predictionData, isLoading }) => {
  const handleExport = () => {
    const csvData = [
      ['Timestamp', 'State', 'District', 'Prediction (MW)', 'Confidence', 'Temperature', 'Humidity'],
      [
        predictionData.timestamp,
        predictionData.state,
        predictionData.district,
        predictionData.current_prediction,
        predictionData.confidence_score,
        predictionData.weather_data.temperature,
        predictionData.weather_data.humidity
      ]
    ];
    
    const csvContent = csvData.map(row => row.join(',')).join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `power_prediction_${predictionData.state}_${Date.now()}.csv`;
    link.click();
  };

  if (isLoading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6">
        {[...Array(4)].map((_, i) => (
          <div key={i} className="bg-white rounded-xl p-6 shadow-sm border border-gray-100 animate-pulse">
            <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
            <div className="h-8 bg-gray-200 rounded w-1/2"></div>
          </div>
        ))}
      </div>
    );
  }

  const cards = [
    {
      title: 'Current Prediction',
      value: `${predictionData.current_prediction.toLocaleString()} MW`,
      icon: Zap,
      color: 'blue',
      trend: '+12.5%',
    },
    {
      title: 'Confidence Score',
      value: `${(predictionData.confidence_score * 100).toFixed(1)}%`,
      icon: Target,
      color: 'green',
      trend: 'High',
    },
    {
      title: '24h Peak Prediction',
      value: `${Math.max(...predictionData.predictions_24h.map(p => p.prediction)).toLocaleString()} MW`,
      icon: TrendingUp,
      color: 'amber',
      trend: '+18.3%',
    },
    {
      title: 'Last Updated',
      value: format(new Date(predictionData.timestamp), 'HH:mm:ss'),
      icon: Clock,
      color: 'cyan',
      trend: 'Live',
    },
  ];

  return (
    <div className="space-y-6">
      {/* Main Prediction Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6">
        {cards.map((card, index) => {
          const Icon = card.icon;
          const colorClasses = {
            blue: 'from-blue-500 to-blue-600 text-white',
            green: 'from-green-500 to-green-600 text-white',
            amber: 'from-amber-500 to-amber-600 text-white',
            cyan: 'from-cyan-500 to-cyan-600 text-white',
          };

          return (
            <div key={index} className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden hover:shadow-md transition-all duration-200">
              <div className={`bg-gradient-to-r ${colorClasses[card.color as keyof typeof colorClasses]} p-4`}>
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-white/80 text-sm font-medium">{card.title}</p>
                    <p className="text-2xl font-bold text-white">{card.value}</p>
                  </div>
                  <Icon className="h-8 w-8 text-white/80" />
                </div>
              </div>
              <div className="p-4">
                <div className="flex items-center justify-between text-sm">
                  <span className="text-gray-600">Trend</span>
                  <span className={`font-medium ${card.color === 'green' ? 'text-green-600' : 'text-blue-600'}`}>
                    {card.trend}
                  </span>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Parameters Grid */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-gray-900">Prediction Parameters</h3>
          <button
            onClick={handleExport}
            className="flex items-center space-x-2 px-3 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            <Download className="h-4 w-4" />
            <span className="text-sm font-medium">Export</span>
          </button>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
          {Object.entries(predictionData.parameters).map(([key, value]) => (
            <div key={key} className="p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
              <p className="text-xs text-gray-600 font-medium uppercase tracking-wide">
                {key.replace(/_/g, ' ')}
              </p>
              <p className="text-lg font-semibold text-gray-900 mt-1">
                {typeof value === 'number' ? value.toLocaleString() : String(value)}
              </p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default PredictionCards;