import paho.mqtt.client as mqtt
import json
from sqlalchemy.orm import Session
from fastapi import Depends
from . import database, crud, schemas

BROKER = 'localhost'
TOPICS = ['temperature_meter/user1', 'temperature_meter/user2', 'temperature_meter/user3']


def create_on_message(db):
    def on_message_closure(client, userdata, msg):
        payload_str = msg.payload.decode()
        print(f"Received message on topic '{msg.topic}': {payload_str}")

        try:
            payload_json = json.loads(payload_str)
            temperature = payload_json.get("temperature")
            if temperature is not None:
                device_id = msg.topic.split("/")[-1]  # Extracting device_id from the topic
                payload = schemas.TemperaturePayload(device_id=device_id, temperature=temperature)
                crud.process_temperature_message(db, payload)
            else:
                print("Invalid JSON format. 'temperature' field is required.")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")

    return on_message_closure


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    for topic in TOPICS:
        client.subscribe(topic)


def on_message(client, userdata, msg, db: Session = Depends(get_db)):
    temp = json.loads(msg.payload.decode())
    print(type(temp))
    print(f"temperature meter: Received message on topic '{msg.topic}': {temp}")
    payload = schemas.TemperaturePayload(device_id="user1", temperature=temp.temperature)
    crud.process_temperature_message(db, payload)


client = mqtt.Client()
client.on_connect = on_connect

client.on_message = create_on_message(next(get_db()))


def connect_mqtt():
    client.connect(BROKER, 1883, 60)
    client.loop_start()


def disconnect_mqtt():
    client.loop_stop()
    client.disconnect()

