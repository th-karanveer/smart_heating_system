import paho.mqtt.client as mqtt

# MQTT broker details
BROKER = 'localhost'
PORT = 1883

# MQTT topics to subscribe to
TOPICS = [
    'heating_system/user1/control',
    'heating_system/user2/control',
    'heating_system/user3/control',
    # Add more topics as needed
]


# Callback function for when a message is received
def on_message(client, userdata, msg):
    print(f"Received message on topic '{msg.topic}': {msg.payload.decode()}")


# Create MQTT client
client = mqtt.Client()

# Set callback function
client.on_message = on_message

# Connect to MQTT broker
client.connect(BROKER, PORT, 60)

# Subscribe to topics
for topic in TOPICS:
    client.subscribe(topic)

# Start MQTT loop to listen for messages
client.loop_forever()
