import sqlite3
import aiosqlite
import asyncio
from datetime import datetime, timedelta
import json
import logging
from pathlib import Path

class Database:
    def __init__(self):
        self.db_path = "data/predictions.db"
        Path("data").mkdir(exist_ok=True)
    
    async def init_db(self):
        """Initialize database tables"""
        async with aiosqlite.connect(self.db_path) as db:
            # Predictions table
            await db.execute("""
                CREATE TABLE IF NOT EXISTS predictions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    state TEXT NOT NULL,
                    district TEXT NOT NULL,
                    prediction REAL NOT NULL,
                    confidence REAL NOT NULL,
                    weather_data TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Historical data table
            await db.execute("""
                CREATE TABLE IF NOT EXISTS historical_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    state TEXT NOT NULL,
                    district TEXT NOT NULL,
                    actual_consumption REAL NOT NULL,
                    weather_data TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            await db.commit()
            logging.info("Database initialized successfully")
    
    async def store_prediction(self, state: str, district: str, prediction: float, 
                             weather_data: dict, confidence: float):
        """Store prediction in database"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute("""
                    INSERT INTO predictions (state, district, prediction, confidence, weather_data)
                    VALUES (?, ?, ?, ?, ?)
                """, (state, district, prediction, confidence, json.dumps(weather_data)))
                await db.commit()
        except Exception as e:
            logging.error(f"Error storing prediction: {e}")
    
    async def get_prediction_history(self, state: str, district: str, days: int = 7):
        """Get historical predictions for visualization"""
        try:
            start_date = datetime.now() - timedelta(days=days)
            
            async with aiosqlite.connect(self.db_path) as db:
                cursor = await db.execute("""
                    SELECT prediction, confidence, weather_data, timestamp
                    FROM predictions
                    WHERE state = ? AND district = ? AND timestamp >= ?
                    ORDER BY timestamp DESC
                    LIMIT 100
                """, (state, district, start_date.isoformat()))
                
                rows = await cursor.fetchall()
                
                history = []
                for row in rows:
                    weather_data = json.loads(row[2])
                    history.append({
                        'prediction': row[0],
                        'confidence': row[1],
                        'temperature': weather_data.get('temperature', 0),
                        'timestamp': row[3]
                    })
                
                return history
                
        except Exception as e:
            logging.error(f"Error fetching history: {e}")
            return []
    
    async def get_historical_data(self, state: str, district: str):
        """Get historical consumption data for context"""
        # For now, return simulated historical data
        # In production, this would fetch actual historical consumption data
        return []