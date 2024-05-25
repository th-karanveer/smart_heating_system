from sqlalchemy import Column, String, Float, Integer, DateTime, func
from .database import Base


class TemperatureReading(Base):
    __tablename__ = "temperature_readings"
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String, index=True)
    temperature = Column(Float)
    timestamp = Column(DateTime, server_default=func.now())


class HeatingSystemState(Base):
    __tablename__ = "heating_system_state"
    device_id = Column(String, primary_key=True, index=True)
    state = Column(String)
