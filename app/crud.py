from sqlalchemy.orm import Session
from sqlalchemy.future import select
from .models import TemperatureReading, HeatingSystemState
from .schemas import TemperaturePayload
from .heating_system_mqtt_client import control_heating_system
import numpy as np
from scipy import stats

WINDOW_SIZE = 100
THRESHOLD = 15.0


def calculate_z_score(data):
    return np.abs(stats.zscore(data))


def process_temperature_message(db: Session, payload: TemperaturePayload):
    db.add(TemperatureReading(device_id=payload.device_id, temperature=payload.temperature))
    db.commit()

    stmt = select(TemperatureReading.temperature).filter(TemperatureReading.device_id == payload.device_id).order_by(TemperatureReading.timestamp.desc()).limit(WINDOW_SIZE)
    result = db.execute(stmt)
    temperatures = [row[0] for row in result.fetchall()]
    if len(temperatures) >= WINDOW_SIZE:
        recent_temps = temperatures[-WINDOW_SIZE:]
        z_scores = calculate_z_score(recent_temps)
        valid_temps = [t for t, z in zip(recent_temps, z_scores) if z < 3]

        if valid_temps:
            avg_temp = sum(valid_temps) / len(valid_temps)
            print(f"average temperature from device {payload.device_id} : {avg_temp}")
            current_state = 'ON' if avg_temp < THRESHOLD else 'OFF'

            heating_state = db.query(HeatingSystemState).filter(HeatingSystemState.device_id == payload.device_id).first()
            if heating_state is None:
                db.add(HeatingSystemState(device_id=payload.device_id, state=current_state))
                db.commit()
                control_heating_system(payload.device_id, current_state)
            elif heating_state.state != current_state:
                heating_state.state = current_state
                db.commit()
                control_heating_system(payload.device_id, current_state)

    return {"message": "Temperature reading processed"}

