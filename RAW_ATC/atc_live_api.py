from flask import Flask, jsonify
import random
import reverse_geocoder as rg
import threading
import time

app = Flask(__name__)

cities = [
    {"name": "New Delhi", "lat": 28.6139, "lon": 77.2090},
    {"name": "Mumbai", "lat": 19.0760, "lon": 72.8777},
    {"name": "Bangalore", "lat": 12.9716, "lon": 77.5946},
    {"name": "Kolkata", "lat": 22.5726, "lon": 88.3639},
    {"name": "Chennai", "lat": 13.0827, "lon": 80.2707},
    {"name": "Hyderabad", "lat": 17.3850, "lon": 78.4867},
    {"name": "Ahmedabad", "lat": 23.0225, "lon": 72.5714},
    {"name": "Jaipur", "lat": 26.9124, "lon": 75.7873},
    {"name": "Pune", "lat": 18.5204, "lon": 73.8567}
]

aircraft_list  = []

def generate_aircraft():
    global aircraft_list
    aircraft_list = []

    for _ in range(15):
        city1 , city2 = random.sample(cities,2)
        lat = city1["lat"]
        lon = city1["lon"]

        aircraft = {
            "icao24" : ''.join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890", k=6)),
            "from" : city1["name"],
            "to" : city2["name"],
            "from_lat" : city1["lat"],
            "from_lon" : city1["lon"],
            "to_lat" : city2["lat"],
            "to_lon" : city2["lon"],
            "latitude" : lat,
            "longitude" : lon,
            "altitude": random.randint(8000, 12000),
            "velocity": random.randint(200, 300),
            "heading": random.randint(0, 359),
            "progress": 0.0,
            "location": "",
            "position_description": ""
        }

        aircraft_list.append(aircraft)

def update_aircraft_positions():
    while True:
        for plane in aircraft_list:
            plane["progress"] = min(1.0, plane["progress"] + 0.02)

            lat = plane["from_lat"] + (plane["to_lat"] - plane["from_"])