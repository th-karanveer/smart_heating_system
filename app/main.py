import uvicorn
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from . import models, crud, schemas, database, heating_system_mqtt_client, temperature_meter_mqtt_subscriber

app = FastAPI()

database.Base.metadata.create_all(bind=database.engine)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
async def startup_event():
    heating_system_mqtt_client.connect_mqtt()
    temperature_meter_mqtt_subscriber.connect_mqtt()


@app.on_event("shutdown")
async def shutdown_event():
    heating_system_mqtt_client.disconnect_mqtt()
    temperature_meter_mqtt_subscriber.disconnect_mqtt()


@app.post("/temperature")
async def receive_temperature(payload: schemas.TemperaturePayload, db: Session = Depends(get_db)):
    return crud.process_temperature_message(db, payload)


if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)

