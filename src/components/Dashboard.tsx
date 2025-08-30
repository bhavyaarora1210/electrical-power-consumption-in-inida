import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import Header from './Header';
import StateSelector from './StateSelector';
import PredictionCards from './PredictionCards';
import ChartsSection from './ChartsSection';
import WeatherPanel from './WeatherPanel';
import { fetchPrediction, fetchStates, fetchHistory } from '../services/api';

const Dashboard: React.FC = () => {
  const [selectedState, setSelectedState] = useState<string>('');
  const [selectedDistrict, setSelectedDistrict] = useState<string>('');

  const { data: statesData } = useQuery({
    queryKey: ['states'],
    queryFn: fetchStates,
  });

  const { data: predictionData, refetch: refetchPrediction, isLoading: predictionLoading } = useQuery({
    queryKey: ['prediction', selectedState, selectedDistrict],
    queryFn: () => fetchPrediction(selectedState, selectedDistrict),
    enabled: !!(selectedState && selectedDistrict),
    refetchInterval: 30000, // Auto-refresh every 30 seconds
  });

  const { data: historyData } = useQuery({
    queryKey: ['history', selectedState, selectedDistrict],
    queryFn: () => fetchHistory(selectedState, selectedDistrict),
    enabled: !!(selectedState && selectedDistrict),
  });

  const handleRefresh = () => {
    refetchPrediction();
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-cyan-50">
      <Header />
      
      <main className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          {/* Left Panel - Controls */}
          <div className="lg:col-span-1 space-y-6">
            <StateSelector
              states={statesData}
              selectedState={selectedState}
              selectedDistrict={selectedDistrict}
              onStateChange={setSelectedState}
              onDistrictChange={setSelectedDistrict}
            />
            
            {predictionData && (
              <WeatherPanel 
                weatherData={predictionData.weather_data}
                onRefresh={handleRefresh}
                isLoading={predictionLoading}
              />
            )}
          </div>

          {/* Main Content */}
          <div className="lg:col-span-3 space-y-6">
            {predictionData && (
              <>
                <PredictionCards 
                  predictionData={predictionData}
                  isLoading={predictionLoading}
                />
                
                <ChartsSection 
                  predictionData={predictionData}
                  historyData={historyData}
                />
              </>
            )}
            
            {!selectedState && (
              <div className="text-center py-20">
                <div className="max-w-md mx-auto">
                  <div className="text-6xl mb-4">⚡</div>
                  <h2 className="text-2xl font-semibold text-gray-800 mb-2">
                    Select Location
                  </h2>
                  <p className="text-gray-600">
                    Choose a state and district to begin real-time power consumption prediction
                  </p>
                </div>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
};

export default Dashboard;