import requests
import random
from faker import Faker

BASE_URL = 'http://127.0.0.1:8000'  # Replace with your FastAPI base URL
fake = Faker()

# Function to create a new Transport
def create_transport():
    url = f"{BASE_URL}/transports/"
    data = {
        "name": fake.company(),
        "speed": random.randint(50, 200),
        "num_cars": random.randint(1, 10),
        "fuel": fake.word(),
    }
    response = requests.post(url, json=data)
    return response.json()

# Function to create a new Route
def create_route():
    url = f"{BASE_URL}/routes/"
    transport_id = random.randint(1, 100)  # Assuming you have 100 transports in the database
    data = {
        "number": fake.word(),
        "passengers": random.randint(10, 200),
        "cost": round(random.uniform(50, 500), 2),
        "num_cars": random.randint(1, 5),
        "transport_id": transport_id,
    }
    response = requests.post(url, json=data)
    return response.json()

# Function to create a new Path
def create_path():
    url = f"{BASE_URL}/paths/"
    route_id = random.randint(1, 100)  # Assuming you have 100 routes in the database
    data = {
        "start": fake.city(),
        "end": fake.city(),
        "stop_numbers": random.randint(2, 10),
        "distance": round(random.uniform(10, 100), 2),
        "route_id": route_id,
    }
    response = requests.post(url, json=data)
    return response.json()

# Creating Transports
for _ in range(50):  # Create 50 Transport entries
    create_transport()

# Creating Routes
for _ in range(100):  # Create 100 Route entries
    create_route()

# Creating Paths
for _ in range(150):  # Create 150 Path entries
    create_path()

