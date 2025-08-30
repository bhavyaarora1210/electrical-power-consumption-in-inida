import httpx
import asyncio
from typing import Dict
import logging

class WeatherService:
    def __init__(self):
        self.base_url = "https://api.open-meteo.com/v1"
        self.geocoding_url = "https://geocoding-api.open-meteo.com/v1"
        
        # Coordinates for major Indian cities
        self.city_coordinates = {
            "Maharashtra": {
                "Mumbai": (19.0760, 72.8777),
                "Pune": (18.5204, 73.8567),
                "Nagpur": (21.1458, 79.0882),
                "Nashik": (19.9975, 73.7898),
                "Aurangabad": (19.8762, 75.3433)
            },
            "Karnataka": {
                "Bangalore": (12.9716, 77.5946),
                "Mysore": (12.2958, 76.6394),
                "Hubli": (15.3647, 75.1240),
                "Mangalore": (12.9141, 74.8560),
                "Belgaum": (15.8497, 74.4977)
            },
            "Tamil Nadu": {
                "Chennai": (13.0827, 80.2707),
                "Coimbatore": (11.0168, 76.9558),
                "Madurai": (9.9252, 78.1198),
                "Salem": (11.6643, 78.1460),
                "Tiruchirappalli": (10.7905, 78.7047)
            },
            "Gujarat": {
                "Ahmedabad": (23.0225, 72.5714),
                "Surat": (21.1702, 72.8311),
                "Vadodara": (22.3072, 73.1812),
                "Rajkot": (22.3039, 70.8022),
                "Gandhinagar": (23.2156, 72.6369)
            },
            "Rajasthan": {
                "Jaipur": (26.9124, 75.7873),
                "Jodhpur": (26.2389, 73.0243),
                "Kota": (25.2138, 75.8648),
                "Bikaner": (28.0229, 73.3119),
                "Udaipur": (24.5854, 73.7125)
            },
            "West Bengal": {
                "Kolkata": (22.5726, 88.3639),
                "Howrah": (22.5958, 88.2636),
                "Durgapur": (23.5204, 87.3119),
                "Asansol": (23.6739, 86.9524),
                "Siliguri": (26.7271, 88.3953)
            },
            "Uttar Pradesh": {
                "Lucknow": (26.8467, 80.9462),
                "Kanpur": (26.4499, 80.3319),
                "Agra": (27.1767, 78.0081),
                "Varanasi": (25.3176, 82.9739),
                "Meerut": (28.9845, 77.7064)
            },
            "Haryana": {
                "Gurgaon": (28.4595, 77.0266),
                "Faridabad": (28.4089, 77.3178),
                "Panipat": (29.3909, 76.9635),
                "Ambala": (30.3782, 76.7767),
                "Hisar": (29.1492, 75.7217)
            },
            "Punjab": {
                "Ludhiana": (30.9010, 75.8573),
                "Amritsar": (31.6340, 74.8723),
                "Jalandhar": (31.3260, 75.5762),
                "Patiala": (30.3398, 76.3869),
                "Bathinda": (30.2110, 74.9455)
            },
            "Delhi": {
                "New Delhi": (28.6139, 77.2090),
                "Central Delhi": (28.6542, 77.2373),
                "South Delhi": (28.5355, 77.2683),
                "North Delhi": (28.7041, 77.1025),
                "East Delhi": (28.6508, 77.3152)
            }
        }
    
    async def get_weather_data(self, state: str, district: str) -> Dict:
        """Fetch current weather data for specified location"""
        try:
            coordinates = self._get_coordinates(state, district)
            if not coordinates:
                # Default to state capital if district not found
                coordinates = list(self.city_coordinates.get(state, {}).values())[0]
            
            lat, lon = coordinates
            
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.get(
                    f"{self.base_url}/forecast",
                    params={
                        "latitude": lat,
                        "longitude": lon,
                        "current": [
                            "temperature_2m",
                            "relative_humidity_2m",
                            "wind_speed_10m",
                            "precipitation"
                        ],
                        "timezone": "Asia/Kolkata"
                    }
                )
                
                response.raise_for_status()
                data = response.json()
                
                current = data.get("current", {})
                
                return {
                    "temperature": current.get("temperature_2m", 25),
                    "humidity": current.get("relative_humidity_2m", 60),
                    "wind_speed": current.get("wind_speed_10m", 10),
                    "rainfall": current.get("precipitation", 0),
                    "location": f"{district}, {state}",
                    "coordinates": f"{lat:.4f}, {lon:.4f}",
                    "last_updated": current.get("time", datetime.now().isoformat())
                }
                
        except Exception as e:
            logging.error(f"Weather data fetch error: {e}")
            # Return default weather data
            return {
                "temperature": 28,
                "humidity": 65,
                "wind_speed": 12,
                "rainfall": 0,
                "location": f"{district}, {state}",
                "coordinates": "0.0000, 0.0000",
                "last_updated": datetime.now().isoformat(),
                "error": "Using simulated weather data"
            }
    
    def _get_coordinates(self, state: str, district: str):
        """Get coordinates for state and district"""
        state_data = self.city_coordinates.get(state)
        if state_data:
            return state_data.get(district)
        return None