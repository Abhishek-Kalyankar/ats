import requests
import struct
import time

# ASTERIX-like binary format: category (B), ICAO (6s), lat, lon, alt, vel, hdg
packet_format = ">B6sfffff"
category = 34
api_url = "http://127.0.0.1:8000/api/aircraft"

def display_aircraft(planes, cycle_num):
    print(f"\n--- CYCLE {cycle_num} ---\n")
    for idx, plane in enumerate(planes, start=1):
        if not all([
            plane.get("icao24"),
            plane.get("latitude"),
            plane.get("longitude"),
            plane.get("altitude"),
            plane.get("velocity"),
            plane.get("heading")
        ]):
            continue

        icao = plane["icao24"][:6].encode("ascii", errors="ignore").ljust(6, b'\x00')
        lat = float(plane["latitude"])
        lon = float(plane["longitude"])
        alt = float(plane["altitude"])
        vel = float(plane["velocity"])
        hdg = float(plane["heading"])
        from_city = plane.get("from", "Unknown")
        to_city = plane.get("to", "Unknown")
        loc = plane.get("location", "Unknown")
        desc = plane.get("position_description", "In flight")

        # Pack and unpack to simulate ASTERIX
        binary_packet = struct.pack(packet_format, category, icao, lat, lon, alt, vel, hdg)
        unpacked = struct.unpack(packet_format, binary_packet)
        cat, icao_bytes, dlat, dlon, dalt, dvel, dhdg = unpacked
        icao_str = icao_bytes.decode("ascii").strip('\x00')

        # Print result
        print(f"{idx}. ICAO        : {icao_str}")
        print(f"   Raw Packet : {binary_packet.hex().upper()}")
        print(f"   Category   : {cat}")
        print(f"   Latitude   : {dlat:.4f}")
        print(f"   Longitude  : {dlon:.4f}")
        print(f"   Altitude   : {dalt} m")
        print(f"   Velocity   : {dvel} m/s")
        print(f"   Heading    : {dhdg}°")
        print(f"   From       : {from_city}")
        print(f"   To         : {to_city}")
        print(f"   Location   : {loc}")
        print(f"   Position   : {desc}")
        print("-" * 60)

def main():
    NUM_CYCLES = 30
    INTERVAL = 10  # seconds

    for cycle in range(1, NUM_CYCLES + 1):
        try:
            resp = requests.get(api_url)
            if resp.status_code != 200:
                print("Failed to fetch aircraft data.")
                time.sleep(INTERVAL)
                continue
            planes = resp.json().get("states", [])
            display_aircraft(planes, cycle)
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()