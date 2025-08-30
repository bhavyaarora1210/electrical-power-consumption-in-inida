import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

def generate_sample_dataset():
    """Generate comprehensive sample dataset for Indian power consumption"""
    np.random.seed(42)
    
    # Define states and districts
    states_districts = {
        "Maharashtra": ["Mumbai", "Pune", "Nagpur", "Nashik", "Aurangabad"],
        "Karnataka": ["Bangalore", "Mysore", "Hubli", "Mangalore", "Belgaum"],
        "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai", "Salem", "Tiruchirappalli"],
        "Gujarat": ["Ahmedabad", "Surat", "Vadodara", "Rajkot", "Gandhinagar"],
        "Rajasthan": ["Jaipur", "Jodhpur", "Kota", "Bikaner", "Udaipur"],
        "West Bengal": ["Kolkata", "Howrah", "Durgapur", "Asansol", "Siliguri"],
        "Uttar Pradesh": ["Lucknow", "Kanpur", "Agra", "Varanasi", "Meerut"],
        "Haryana": ["Gurgaon", "Faridabad", "Panipat", "Ambala", "Hisar"],
        "Punjab": ["Ludhiana", "Amritsar", "Jalandhar", "Patiala", "Bathinda"],
        "Delhi": ["New Delhi", "Central Delhi", "South Delhi", "North Delhi", "East Delhi"]
    }
    
    # Base consumption by state (MW)
    state_base_consumption = {
        "Maharashtra": 18000, "Karnataka": 12000, "Tamil Nadu": 14000,
        "Gujarat": 13000, "Rajasthan": 8000, "West Bengal": 9000,
        "Uttar Pradesh": 16000, "Haryana": 6000, "Punjab": 7000, "Delhi": 5000
    }
    
    # Population factors by district (relative to state average)
    district_population_factors = {
        "Mumbai": 1.8, "Chennai": 1.6, "Bangalore": 1.7, "Kolkata": 1.5,
        "New Delhi": 1.4, "Ahmedabad": 1.3, "Pune": 1.2, "Lucknow": 1.1,
        "Jaipur": 1.2, "Ludhiana": 1.0
    }
    
    data = []
    
    # Generate data for past 2 years
    start_date = datetime.now() - timedelta(days=730)
    
    for day_offset in range(730):
        current_date = start_date + timedelta(days=day_offset)
        
        for state, districts in states_districts.items():
            for district in districts:
                for hour in range(0, 24, 3):  # Every 3 hours
                    # Base consumption
                    base_consumption = state_base_consumption[state]
                    
                    # Population factor
                    pop_factor = district_population_factors.get(
                        district.split("_")[0] if "_" in district else district, 1.0
                    )
                    
                    # Seasonal weather simulation
                    month = current_date.month
                    
                    if month in [4, 5, 6]:  # Summer
                        temp_base = 35
                        humidity_base = 45
                        rainfall = np.random.exponential(0.5)
                    elif month in [7, 8, 9]:  # Monsoon
                        temp_base = 28
                        humidity_base = 80
                        rainfall = np.random.exponential(10)
                    elif month in [12, 1, 2]:  # Winter
                        temp_base = 20
                        humidity_base = 60
                        rainfall = np.random.exponential(0.2)
                    else:  # Spring/Post-monsoon
                        temp_base = 26
                        humidity_base = 65
                        rainfall = np.random.exponential(2)
                    
                    # Weather with daily variation
                    temperature = temp_base + np.random.normal(0, 5)
                    humidity = max(20, min(95, humidity_base + np.random.normal(0, 15)))
                    wind_speed = np.random.uniform(5, 25)
                    
                    # Time factors
                    time_factor = 1.0
                    if 6 <= hour <= 9 or 18 <= hour <= 22:  # Peak hours
                        time_factor = np.random.uniform(1.5, 1.9)
                    elif 22 <= hour <= 24 or 0 <= hour <= 6:  # Night
                        time_factor = np.random.uniform(0.5, 0.7)
                    else:  # Day
                        time_factor = np.random.uniform(1.0, 1.4)
                    
                    # Weekend factor
                    weekend_factor = 0.8 if current_date.weekday() >= 5 else 1.0
                    
                    # Temperature effect (AC usage)
                    if temperature > 30:
                        ac_factor = 1 + (temperature - 30) * 0.04
                    elif temperature < 15:
                        heating_factor = 1 + (15 - temperature) * 0.02
                        ac_factor = heating_factor
                    else:
                        ac_factor = 1.0
                    
                    # Industrial load
                    industrial_base = {
                        "Maharashtra": 0.85, "Karnataka": 0.75, "Tamil Nadu": 0.80,
                        "Gujarat": 0.90, "Rajasthan": 0.60, "West Bengal": 0.70,
                        "Uttar Pradesh": 0.65, "Haryana": 0.75, "Punjab": 0.70, "Delhi": 0.55
                    }
                    industrial_load = industrial_base[state] * weekend_factor
                    
                    # Calculate final consumption
                    consumption = (base_consumption * pop_factor * time_factor * 
                                 ac_factor * industrial_load * 
                                 np.random.uniform(0.9, 1.1))
                    
                    data.append({
                        'timestamp': current_date.replace(hour=hour),
                        'state': state,
                        'district': district,
                        'temperature': round(temperature, 2),
                        'humidity': round(humidity, 2),
                        'wind_speed': round(wind_speed, 2),
                        'rainfall': round(rainfall, 2),
                        'population_factor': round(pop_factor, 3),
                        'industrial_load': round(industrial_load, 3),
                        'hour': hour,
                        'day_of_week': current_date.weekday(),
                        'month': month,
                        'is_weekend': int(current_date.weekday() >= 5),
                        'power_consumption_mw': round(consumption, 2)
                    })
    
    df = pd.DataFrame(data)
    df.to_csv("data/india_power_consumption_dataset.csv", index=False)
    
    # Create summary statistics
    summary = {
        "total_records": len(df),
        "date_range": {
            "start": df['timestamp'].min().isoformat(),
            "end": df['timestamp'].max().isoformat()
        },
        "states_covered": list(df['state'].unique()),
        "avg_consumption_by_state": df.groupby('state')['power_consumption_mw'].mean().round(2).to_dict(),
        "weather_ranges": {
            "temperature": {"min": df['temperature'].min(), "max": df['temperature'].max()},
            "humidity": {"min": df['humidity'].min(), "max": df['humidity'].max()},
            "wind_speed": {"min": df['wind_speed'].min(), "max": df['wind_speed'].max()},
            "rainfall": {"min": df['rainfall'].min(), "max": df['rainfall'].max()}
        }
    }
    
    with open("data/dataset_summary.json", "w") as f:
        json.dump(summary, f, indent=2, default=str)
    
    print(f"Generated dataset with {len(df)} records")
    print(f"Date range: {summary['date_range']['start']} to {summary['date_range']['end']}")
    return df

if __name__ == "__main__":
    generate_sample_dataset()