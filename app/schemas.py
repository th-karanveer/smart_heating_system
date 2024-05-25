from pydantic import BaseModel


class TemperaturePayload(BaseModel):
    device_id: str
    temperature: float
