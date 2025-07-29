from sqlalchemy import Column, Integer, String, DateTime
import datetime
from app.db.session import Base

class WeatherData(Base):
    __tablename__ = "weather_data"
    
    id = Column(Integer, primary_key=True, index=True)
    location = Column(String, index=True, default="서울")
    current_temp = Column(String)
    weather_status = Column(String)
    air_quality = Column(String)
    crawled_at = Column(DateTime, default=datetime.datetime.now)