const API_BASE_URL = 'http://localhost:8000/api';

export interface PredictionData {
  state: string;
  district: string;
  current_prediction: number;
  confidence_score: number;
  weather_data: any;
  parameters: any;
  predictions_24h: any[];
  timestamp: string;
}

export const fetchStates = async (): Promise<Record<string, string[]>> => {
  try {
    const response = await fetch(`${API_BASE_URL}/states`);
    if (!response.ok) {
      throw new Error('Failed to fetch states');
    }
    return await response.json();
  } catch (error) {
    console.error('Error fetching states:', error);
    // Return fallback data
    return {
      "Maharashtra": ["Mumbai", "Pune", "Nagpur", "Nashik", "Aurangabad"],
      "Karnataka": ["Bangalore", "Mysore", "Hubli", "Mangalore", "Belgaum"],
      "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai", "Salem", "Tiruchirappalli"],
      "Gujarat": ["Ahmedabad", "Surat", "Vadodara", "Rajkot", "Gandhinagar"],
      "Delhi": ["New Delhi", "Central Delhi", "South Delhi", "North Delhi", "East Delhi"]
    };
  }
};

export const fetchPrediction = async (state: string, district: string): Promise<PredictionData> => {
  try {
    const response = await fetch(`${API_BASE_URL}/predict`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ state, district }),
    });
    
    if (!response.ok) {
      throw new Error('Failed to fetch prediction');
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error fetching prediction:', error);
    // Return mock data for demo purposes
    return {
      state,
      district,
      current_prediction: Math.round(Math.random() * 15000 + 5000),
      confidence_score: 0.85 + Math.random() * 0.1,
      weather_data: {
        temperature: 28 + Math.random() * 10,
        humidity: 60 + Math.random() * 20,
        wind_speed: 10 + Math.random() * 10,
        rainfall: Math.random() * 5,
        location: `${district}, ${state}`,
        last_updated: new Date().toISOString(),
        error: "Using simulated data - backend not available"
      },
      parameters: {
        temperature: 32.5,
        humidity: 68,
        wind_speed: 12.3,
        rainfall: 0.0,
        industrial_load: 0.785,
        hour: new Date().getHours(),
        is_peak_hour: true,
        is_weekend: false,
        season: 'Summer'
      },
      predictions_24h: Array.from({ length: 24 }, (_, i) => ({
        hour_offset: i + 1,
        timestamp: new Date(Date.now() + (i + 1) * 60 * 60 * 1000).toISOString(),
        prediction: Math.round(Math.random() * 15000 + 5000),
        hour: (new Date().getHours() + i + 1) % 24
      })),
      timestamp: new Date().toISOString()
    };
  }
};

export const fetchHistory = async (state: string, district: string) => {
  try {
    const response = await fetch(`${API_BASE_URL}/history/${state}/${district}`);
    if (!response.ok) {
      throw new Error('Failed to fetch history');
    }
    return await response.json();
  } catch (error) {
    console.error('Error fetching history:', error);
    // Return mock historical data
    const mockHistory = Array.from({ length: 20 }, (_, i) => ({
      prediction: Math.round(Math.random() * 15000 + 5000),
      confidence: 0.8 + Math.random() * 0.2,
      temperature: 25 + Math.random() * 15,
      timestamp: new Date(Date.now() - i * 60 * 60 * 1000).toISOString()
    }));
    
    return { history: mockHistory };
  }
};