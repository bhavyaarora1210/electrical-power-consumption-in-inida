import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import joblib
import asyncio
from datetime import datetime, timedelta
import logging
from pathlib import Path

class PowerConsumptionPredictor:
    def __init__(self):
        self.rf_model = None
        self.gb_model = None
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.is_trained = False
        self.feature_names = []
        
    async def load_model(self):
        """Load pre-trained model or train new one"""
        model_path = Path("models/trained_model.joblib")
        
        if model_path.exists():
            try:
                model_data = joblib.load(model_path)
                self.rf_model = model_data['rf_model']
                self.gb_model = model_data['gb_model']
                self.scaler = model_data['scaler']
                self.label_encoders = model_data['label_encoders']
                self.feature_names = model_data['feature_names']
                self.is_trained = True
                logging.info("Model loaded successfully")
            except Exception as e:
                logging.warning(f"Could not load model: {e}")
                await self.train_model()
        else:
            await self.train_model()
    
    async def train_model(self):
        """Train the prediction model"""
        try:
            # Generate synthetic training data
            data = self._generate_synthetic_data()
            
            # Prepare features
            X, y = self._prepare_features(data)
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            # Train models
            self.rf_model = RandomForestRegressor(
                n_estimators=100, 
                random_state=42,
                max_depth=10,
                min_samples_split=5
            )
            self.gb_model = GradientBoostingRegressor(
                n_estimators=100,
                random_state=42,
                max_depth=6,
                learning_rate=0.1
            )
            
            self.rf_model.fit(X_train, y_train)
            self.gb_model.fit(X_train, y_train)
            
            # Evaluate models
            rf_pred = self.rf_model.predict(X_test)
            gb_pred = self.gb_model.predict(X_test)
            
            rf_mae = mean_absolute_error(y_test, rf_pred)
            gb_mae = mean_absolute_error(y_test, gb_pred)
            
            logging.info(f"Random Forest MAE: {rf_mae:.2f}")
            logging.info(f"Gradient Boosting MAE: {gb_mae:.2f}")
            
            # Save model
            Path("models").mkdir(exist_ok=True)
            joblib.dump({
                'rf_model': self.rf_model,
                'gb_model': self.gb_model,
                'scaler': self.scaler,
                'label_encoders': self.label_encoders,
                'feature_names': self.feature_names
            }, "models/trained_model.joblib")
            
            self.is_trained = True
            logging.info("Model training completed successfully")
            
        except Exception as e:
            logging.error(f"Error training model: {e}")
            raise
    
    def _generate_synthetic_data(self):
        """Generate synthetic training data based on Indian power consumption patterns"""
        np.random.seed(42)
        n_samples = 10000
        
        states = ["Maharashtra", "Karnataka", "Tamil Nadu", "Gujarat", "Rajasthan", 
                 "West Bengal", "Uttar Pradesh", "Haryana", "Punjab", "Delhi"]
        districts_per_state = 5
        
        data = []
        
        for i in range(n_samples):
            state = np.random.choice(states)
            district_idx = np.random.randint(0, districts_per_state)
            
            # Base consumption by state (MW)
            state_base = {
                "Maharashtra": 18000, "Karnataka": 12000, "Tamil Nadu": 14000,
                "Gujarat": 13000, "Rajasthan": 8000, "West Bengal": 9000,
                "Uttar Pradesh": 16000, "Haryana": 6000, "Punjab": 7000, "Delhi": 5000
            }
            
            base_consumption = state_base[state]
            
            # Time factors
            hour = np.random.randint(0, 24)
            day_of_week = np.random.randint(0, 7)
            month = np.random.randint(1, 13)
            
            # Weather parameters
            temperature = np.random.normal(28, 8)  # Celsius
            humidity = np.random.uniform(30, 90)   # %
            wind_speed = np.random.uniform(2, 20)  # km/h
            rainfall = np.random.exponential(2)     # mm
            
            # Seasonal adjustments
            if month in [4, 5, 6]:  # Summer
                temperature += np.random.normal(8, 2)
                base_consumption *= np.random.uniform(1.3, 1.6)
            elif month in [12, 1, 2]:  # Winter
                temperature -= np.random.normal(5, 2)
                base_consumption *= np.random.uniform(0.8, 1.1)
            elif month in [7, 8, 9]:  # Monsoon
                rainfall += np.random.exponential(5)
                humidity += np.random.normal(10, 5)
                base_consumption *= np.random.uniform(0.9, 1.2)
            
            # Time of day effects
            if 6 <= hour <= 9 or 18 <= hour <= 22:  # Peak hours
                time_factor = np.random.uniform(1.4, 1.8)
            elif 22 <= hour <= 24 or 0 <= hour <= 6:  # Night
                time_factor = np.random.uniform(0.6, 0.8)
            else:  # Day
                time_factor = np.random.uniform(1.0, 1.3)
            
            # Industrial/commercial factors
            industrial_load = np.random.uniform(0.7, 1.3)
            if day_of_week >= 5:  # Weekend
                industrial_load *= 0.7
            
            # Temperature effect on AC usage
            if temperature > 30:
                ac_factor = 1 + (temperature - 30) * 0.05
            elif temperature < 15:
                heating_factor = 1 + (15 - temperature) * 0.03
                ac_factor = heating_factor
            else:
                ac_factor = 1.0
            
            # Calculate final consumption
            consumption = (base_consumption * time_factor * industrial_load * 
                         ac_factor * np.random.uniform(0.9, 1.1))
            
            data.append({
                'state': state,
                'district': f"{state}_District_{district_idx + 1}",
                'hour': hour,
                'day_of_week': day_of_week,
                'month': month,
                'temperature': round(temperature, 2),
                'humidity': round(humidity, 2),
                'wind_speed': round(wind_speed, 2),
                'rainfall': round(rainfall, 2),
                'industrial_load': round(industrial_load, 3),
                'power_consumption_mw': round(consumption, 2)
            })
        
        return pd.DataFrame(data)
    
    def _prepare_features(self, data):
        """Prepare features for training"""
        # Create label encoders
        categorical_cols = ['state', 'district']
        for col in categorical_cols:
            if col not in self.label_encoders:
                self.label_encoders[col] = LabelEncoder()
            data[col + '_encoded'] = self.label_encoders[col].fit_transform(data[col])
        
        # Feature engineering
        data['temp_squared'] = data['temperature'] ** 2
        data['humidity_temp'] = data['humidity'] * data['temperature']
        data['is_peak_hour'] = ((data['hour'] >= 6) & (data['hour'] <= 9) | 
                               (data['hour'] >= 18) & (data['hour'] <= 22)).astype(int)
        data['is_weekend'] = (data['day_of_week'] >= 5).astype(int)
        data['season'] = data['month'].apply(self._get_season)
        
        # Select features
        feature_cols = [
            'state_encoded', 'district_encoded', 'hour', 'day_of_week', 'month',
            'temperature', 'humidity', 'wind_speed', 'rainfall', 'industrial_load',
            'temp_squared', 'humidity_temp', 'is_peak_hour', 'is_weekend', 'season'
        ]
        
        self.feature_names = feature_cols
        X = data[feature_cols].values
        y = data['power_consumption_mw'].values
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        return X_scaled, y
    
    def _get_season(self, month):
        if month in [3, 4, 5]:
            return 1  # Summer
        elif month in [6, 7, 8, 9]:
            return 2  # Monsoon
        elif month in [10, 11]:
            return 3  # Post-monsoon
        else:
            return 4  # Winter
    
    async def predict(self, state: str, district: str, weather_data: dict, historical_data: list):
        """Make power consumption prediction"""
        if not self.is_trained:
            raise Exception("Model not trained")
        
        try:
            # Prepare input features
            current_time = datetime.now()
            
            # Encode categorical variables
            state_encoded = self._encode_categorical('state', state)
            district_encoded = self._encode_categorical('district', district)
            
            # Extract weather features
            temperature = weather_data.get('temperature', 25)
            humidity = weather_data.get('humidity', 60)
            wind_speed = weather_data.get('wind_speed', 10)
            rainfall = weather_data.get('rainfall', 0)
            
            # Calculate industrial load (simulated)
            industrial_load = self._calculate_industrial_load(state, current_time)
            
            # Feature engineering
            temp_squared = temperature ** 2
            humidity_temp = humidity * temperature
            is_peak_hour = int(6 <= current_time.hour <= 9 or 18 <= current_time.hour <= 22)
            is_weekend = int(current_time.weekday() >= 5)
            season = self._get_season(current_time.month)
            
            # Prepare feature vector
            features = np.array([[
                state_encoded, district_encoded, current_time.hour, current_time.weekday(),
                current_time.month, temperature, humidity, wind_speed, rainfall,
                industrial_load, temp_squared, humidity_temp, is_peak_hour, is_weekend, season
            ]])
            
            # Scale features
            features_scaled = self.scaler.transform(features)
            
            # Make predictions with both models
            rf_pred = self.rf_model.predict(features_scaled)[0]
            gb_pred = self.gb_model.predict(features_scaled)[0]
            
            # Ensemble prediction (weighted average)
            final_prediction = 0.6 * rf_pred + 0.4 * gb_pred
            
            # Calculate confidence score
            pred_std = np.abs(rf_pred - gb_pred)
            confidence = max(0.5, 1 - (pred_std / final_prediction))
            
            return {
                'prediction': round(final_prediction, 2),
                'confidence': round(confidence, 3),
                'parameters': {
                    'temperature': temperature,
                    'humidity': humidity,
                    'wind_speed': wind_speed,
                    'rainfall': rainfall,
                    'industrial_load': round(industrial_load, 3),
                    'hour': current_time.hour,
                    'is_peak_hour': bool(is_peak_hour),
                    'is_weekend': bool(is_weekend),
                    'season': ['', 'Summer', 'Monsoon', 'Post-monsoon', 'Winter'][season]
                }
            }
            
        except Exception as e:
            logging.error(f"Prediction error: {e}")
            raise
    
    async def predict_24h(self, state: str, district: str, weather_data: dict):
        """Generate 24-hour ahead predictions"""
        predictions = []
        
        for hour_offset in range(1, 25):
            future_time = datetime.now() + timedelta(hours=hour_offset)
            
            # Simulate future weather (slight variations)
            temp_variation = np.random.normal(0, 2)
            future_weather = {
                'temperature': weather_data['temperature'] + temp_variation,
                'humidity': max(20, min(100, weather_data['humidity'] + np.random.normal(0, 5))),
                'wind_speed': max(0, weather_data['wind_speed'] + np.random.normal(0, 3)),
                'rainfall': max(0, weather_data['rainfall'] + np.random.normal(0, 1))
            }
            
            # Make prediction for future time
            prediction = await self._predict_for_time(
                state, district, future_weather, future_time
            )
            
            predictions.append({
                'hour_offset': hour_offset,
                'timestamp': future_time.isoformat(),
                'prediction': prediction,
                'hour': future_time.hour
            })
        
        return predictions
    
    async def _predict_for_time(self, state: str, district: str, weather_data: dict, target_time: datetime):
        """Make prediction for specific time"""
        if not self.is_trained:
            return 0
        
        try:
            state_encoded = self._encode_categorical('state', state)
            district_encoded = self._encode_categorical('district', district)
            
            temperature = weather_data['temperature']
            humidity = weather_data['humidity']
            wind_speed = weather_data['wind_speed']
            rainfall = weather_data['rainfall']
            
            industrial_load = self._calculate_industrial_load(state, target_time)
            
            features = np.array([[
                state_encoded, district_encoded, target_time.hour, target_time.weekday(),
                target_time.month, temperature, humidity, wind_speed, rainfall,
                industrial_load, temperature ** 2, humidity * temperature,
                int(6 <= target_time.hour <= 9 or 18 <= target_time.hour <= 22),
                int(target_time.weekday() >= 5), self._get_season(target_time.month)
            ]])
            
            features_scaled = self.scaler.transform(features)
            
            rf_pred = self.rf_model.predict(features_scaled)[0]
            gb_pred = self.gb_model.predict(features_scaled)[0]
            
            return round(0.6 * rf_pred + 0.4 * gb_pred, 2)
            
        except Exception as e:
            logging.error(f"Time-specific prediction error: {e}")
            return 0
    
    def _encode_categorical(self, column: str, value: str):
        """Encode categorical variable"""
        if column not in self.label_encoders:
            return 0
        
        try:
            return self.label_encoders[column].transform([value])[0]
        except:
            # Return most common class if unseen value
            return 0
    
    def _calculate_industrial_load(self, state: str, time: datetime):
        """Calculate industrial load factor"""
        base_industrial = {
            "Maharashtra": 0.85, "Karnataka": 0.75, "Tamil Nadu": 0.80,
            "Gujarat": 0.90, "Rajasthan": 0.60, "West Bengal": 0.70,
            "Uttar Pradesh": 0.65, "Haryana": 0.75, "Punjab": 0.70, "Delhi": 0.55
        }
        
        base = base_industrial.get(state, 0.70)
        
        # Reduce on weekends
        if time.weekday() >= 5:
            base *= 0.7
        
        # Reduce at night
        if 22 <= time.hour or time.hour <= 6:
            base *= 0.6
        
        return base + np.random.normal(0, 0.1)