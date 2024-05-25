import requests
import random
import time

# API endpoint URL
API_URL = "http://localhost:8000/temperature"

# Number of samples to generate
NUM_SAMPLES = 600

# List of device IDs for testing
DEVICE_IDS = ["user1", "user2", "user3"]


# Function to generate random temperature data
def generate_temperature_data():
    return round(random.uniform(10, 25), 2)


# Function to generate test data samples
def generate_test_data(num_samples):
    test_data = []
    for _ in range(num_samples):
        payload = {
            "device_id": random.choice(DEVICE_IDS),
            "temperature": generate_temperature_data()
        }
        test_data.append(payload)
    return test_data


# Function to send test data to the API
def send_test_data(test_data):
    for payload in test_data:
        response = requests.post(API_URL, json=payload)
        if response.status_code == 200:
            print(f"Temperature reading processed: {payload}")
        else:
            print(f"Failed to process temperature reading: {payload}")


if __name__ == "__main__":
    test_data = generate_test_data(NUM_SAMPLES)
    send_test_data(test_data)
