from flask import Flask, jsonify
import random
from flask_cors import CORS
import reverse_geocoder as rg
import threading
import time

app = Flask(__name__)
CORS(app) 

# Static city list
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

# Global aircraft list
aircraft_list = []

def generate_aircraft():
    global aircraft_list
    aircraft_list = []

    for _ in range(15):
        city1, city2 = random.sample(cities, 2)
        lat = city1["lat"]
        lon = city1["lon"]

        aircraft = {
            "icao24": ''.join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=6)),
            "from": city1["name"],
            "to": city2["name"],
            "from_lat": city1["lat"],
            "from_lon": city1["lon"],
            "to_lat": city2["lat"],
            "to_lon": city2["lon"],
            "latitude": lat,
            "longitude": lon,
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
            # Update progress
            plane["progress"] = min(1.0, plane["progress"] + 0.02)

            # Move position
            lat = plane["from_lat"] + (plane["to_lat"] - plane["from_lat"]) * plane["progress"]
            lon = plane["from_lon"] + (plane["to_lon"] - plane["from_lon"]) * plane["progress"]
            plane["latitude"] = lat
            plane["longitude"] = lon

            # Update altitude (simulate descent)
            if plane["progress"] >= 0.8:
                plane["altitude"] = max(1000, plane["altitude"] - 300)

            # Reverse geocode
            try:
                result = rg.search((lat, lon), mode=1)[0]
                location_name = f"{result['name']}, {result['admin1']}, {result['cc']}"
            except:
                location_name = "Unknown"

            plane["location"] = location_name
            plane["position_description"] = f"Flying from {plane['from']} to {plane['to']} near {location_name} ({int(plane['progress']*100)}%)"

        time.sleep(10)

@app.route('/api/aircraft')
def get_aircraft():
    return jsonify({"states": aircraft_list})

if __name__ == '__main__':
    generate_aircraft()
    updater_thread = threading.Thread(target=update_aircraft_positions)
    updater_thread.daemon = True
    updater_thread.start()
    
    import os
    port = int(os.environ.get('PORT', 8000))  # Default to 8000 if PORT is not set
    app.run(debug=False, host='0.0.0.0', port=port)
