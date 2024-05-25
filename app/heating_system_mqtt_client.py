import json
import paho.mqtt.client as mqtt

BROKER = 'localhost'
client = mqtt.Client()


def connect_mqtt():
    client.connect(BROKER, 1883, 60)
    client.loop_start()


def disconnect_mqtt():
    client.loop_stop()
    client.disconnect()


def control_heating_system(device_id, state):
    try:
        control_message = json.dumps({
            'action': state
        })
        topic = f'heating_system/{device_id}/control'
        print(f"heating system: Published message on topic: {topic} for device_id {device_id} with state {state}")
        client.publish(topic, control_message)
    except Exception as exx:
        print(f"Exception in control_heating_system: {exx}")
