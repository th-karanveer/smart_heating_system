# Smart Heating System

## Overview

This project implements a smart heating system using FastAPI, PostgreSQL, and MQTT (mosquitto as localhost mqtt broker, paho as python mqtt client and subscriber).

## Setup

1. create env and Install dependencies:
    ```bash
    git clone https://github.com/th-karanveer/smart_heating_system
    cd smart_heating_system
    python -m venv env
    source env/bin/activate
    pip install -r requirements.txt
    ```
   
2. Initiate Alembic to manage db and migrations:
   ```base
   alembic init alembic
   ```
   
3. Set up the PostgreSQL database and create db `smart_heating`. Update the following in project: 
   `DATABASE_URL` in `app/database.py`
   `sqlalchemy.url` in `alembic.ini`

   for example: "postgresql://user:password@localhost/smart_heating"
   note: update user and password in the above url and make sure the user has permissions for the respective database

4. Run Migrations:
   ```base
   alembic revision --autogenerate -m "Initial migration"
   alembic upgrade head
   ```
5. Update the mqtt broker host respectively in `app.heating_system_mqtt_client.py` & `temperature_meter_mqtt_subscriber.py` for example BROKER = 'localhost'

6. Run the FastAPI application:
    ```bash
    uvicorn app.main:app --reload
    ```

7. Run ` python scripts.generate_test_data.py` to generate sample entries in Database for the decision component to work
   (NOTE: OPTIONAL & FOR TESTING PURPOSE ONLY)
