from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import pandas as pd
import numpy as np
import asyncio
import httpx
from datetime import datetime, timedelta
import json
import sqlite3
from pathlib import Path
import os

from models.prediction_model import PowerConsumptionPredictor
from models.weather_service import WeatherService
from models.database import Database

app = FastAPI(title="India Power Consumption Prediction API", version="1.0.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
weather_service = WeatherService()
predictor = PowerConsumptionPredictor()
database = Database()

class PredictionRequest(BaseModel):
    state: str
    district: str

class PredictionResponse(BaseModel):
    state: str
    district: str
    current_prediction: float
    confidence_score: float
    weather_data: dict
    parameters: dict
    predictions_24h: List[dict]
    timestamp: str

@app.on_event("startup")
async def startup_event():
    await database.init_db()
    await predictor.load_model()

@app.get("/api/states")
async def get_states():
    """Get list of available states"""
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
    return states_districts

@app.post("/api/predict", response_model=PredictionResponse)
async def predict_consumption(request: PredictionRequest):
    """Predict power consumption for given state and district"""
    try:
        # Get weather data
        weather_data = await weather_service.get_weather_data(request.state, request.district)
        
        # Get historical context
        historical_data = await database.get_historical_data(request.state, request.district)
        
        # Make prediction
        prediction_result = await predictor.predict(
            state=request.state,
            district=request.district,
            weather_data=weather_data,
            historical_data=historical_data
        )
        
        # Get 24-hour predictions
        predictions_24h = await predictor.predict_24h(
            state=request.state,
            district=request.district,
            weather_data=weather_data
        )
        
        # Store prediction in database
        await database.store_prediction(
            state=request.state,
            district=request.district,
            prediction=prediction_result['prediction'],
            weather_data=weather_data,
            confidence=prediction_result['confidence']
        )
        
        return PredictionResponse(
            state=request.state,
            district=request.district,
            current_prediction=prediction_result['prediction'],
            confidence_score=prediction_result['confidence'],
            weather_data=weather_data,
            parameters=prediction_result['parameters'],
            predictions_24h=predictions_24h,
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/history/{state}/{district}")
async def get_history(state: str, district: str, days: int = 7):
    """Get historical predictions for visualization"""
    try:
        history = await database.get_prediction_history(state, district, days)
        return {"history": history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)