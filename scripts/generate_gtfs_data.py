"""Mock GTFS (General Transit Feed Specification) data generator

Generates realistic mock public transportation data for Cairo Metro system.
Creates NDJSON file at `data/gtfs_data.ndjson`.

GTFS Standard Reference: https://gtfs.org/reference/static

Usage:
    python scripts/generate_gtfs_data.py --trips 100
"""
import argparse
import json
import random
from datetime import datetime, timezone, timedelta, time
from pathlib import Path

OUT_DIR = Path("data")
OUT_FILE = OUT_DIR / "gtfs_data.ndjson"

# Cairo Metro Lines (Agencies)
AGENCIES = [
    {"agency_id": "cairo_metro", "agency_name": "Cairo Metro", "agency_timezone": "Africa/Cairo"},
]

# Cairo Metro Routes (Simplified - 3 main lines)
ROUTES = [
    {"route_id": "L1", "route_short_name": "Line 1", "route_long_name": "Helwan - El Marg", "route_type": 1, "route_color": "FF0000"},
    {"route_id": "L2", "route_short_name": "Line 2", "route_long_name": "Shobra El Kheima - El Mounib", "route_type": 1, "route_color": "FFFF00"},
    {"route_id": "L3", "route_short_name": "Line 3", "route_long_name": "Adly Mansour - Imbaba", "route_type": 1, "route_color": "00FF00"},
]

# Sample stops for each line (simplified)
STOPS = {
    "L1": [
        {"stop_id": "L1_S01", "stop_name": "Helwan", "stop_lat": 29.8489, "stop_lon": 31.3342},
        {"stop_id": "L1_S02", "stop_name": "Ain Helwan", "stop_lat": 29.8627, "stop_lon": 31.3251},
        {"stop_id": "L1_S03", "stop_name": "Helwan University", "stop_lat": 29.8695, "stop_lon": 31.3199},
        {"stop_id": "L1_S04", "stop_name": "Wadi Hof", "stop_lat": 29.8793, "stop_lon": 31.3137},
        {"stop_id": "L1_S05", "stop_name": "Hadayek Helwan", "stop_lat": 29.8972, "stop_lon": 31.3043},
        {"stop_id": "L1_S06", "stop_name": "El Maasara", "stop_lat": 29.9062, "stop_lon": 31.2990},
        {"stop_id": "L1_S07", "stop_name": "Tora El Asmant", "stop_lat": 29.9168, "stop_lon": 31.2927},
        {"stop_id": "L1_S08", "stop_name": "Kozzika", "stop_lat": 29.9245, "stop_lon": 31.2880},
        {"stop_id": "L1_S09", "stop_name": "Tora El Balad", "stop_lat": 29.9348, "stop_lon": 31.2814},
        {"stop_id": "L1_S10", "stop_name": "Sakanat El Maadi", "stop_lat": 29.9531, "stop_lon": 31.2634},
        {"stop_id": "L1_S11", "stop_name": "Maadi", "stop_lat": 29.9604, "stop_lon": 31.2577},
        {"stop_id": "L1_S12", "stop_name": "Hadayek El Maadi", "stop_lat": 29.9703, "stop_lon": 31.2504},
        {"stop_id": "L1_S13", "stop_name": "Dar El Salam", "stop_lat": 29.9820, "stop_lon": 31.2421},
        {"stop_id": "L1_S14", "stop_name": "El Zahraa", "stop_lat": 29.9954, "stop_lon": 31.2314},
        {"stop_id": "L1_S15", "stop_name": "Mar Girgis", "stop_lat": 30.0061, "stop_lon": 31.2295},
        {"stop_id": "L1_S16", "stop_name": "El Malek El Saleh", "stop_lat": 30.0174, "stop_lon": 31.2312},
        {"stop_id": "L1_S17", "stop_name": "Al Sayeda Zeinab", "stop_lat": 30.0293, "stop_lon": 31.2354},
        {"stop_id": "L1_S18", "stop_name": "Saad Zaghloul", "stop_lat": 30.0372, "stop_lon": 31.2381},
        {"stop_id": "L1_S19", "stop_name": "Sadat", "stop_lat": 30.0442, "stop_lon": 31.2347},  # Transfer station
        {"stop_id": "L1_S20", "stop_name": "Nasser", "stop_lat": 30.0535, "stop_lon": 31.2389},
        {"stop_id": "L1_S21", "stop_name": "Orabi", "stop_lat": 30.0570, "stop_lon": 31.2423},
        {"stop_id": "L1_S22", "stop_name": "Al Shohadaa", "stop_lat": 30.0611, "stop_lon": 31.2458},  # Transfer station
        {"stop_id": "L1_S23", "stop_name": "Ghamra", "stop_lat": 30.0687, "stop_lon": 31.2648},
        {"stop_id": "L1_S24", "stop_name": "El Demerdash", "stop_lat": 30.0773, "stop_lon": 31.2779},
        {"stop_id": "L1_S25", "stop_name": "Manshiet El Sadr", "stop_lat": 30.0822, "stop_lon": 31.2875},
        {"stop_id": "L1_S26", "stop_name": "Kobri El Qobba", "stop_lat": 30.0873, "stop_lon": 31.2943},
        {"stop_id": "L1_S27", "stop_name": "Hammamat El Qobba", "stop_lat": 30.0914, "stop_lon": 31.2994},
        {"stop_id": "L1_S28", "stop_name": "Saray El Qobba", "stop_lat": 30.0976, "stop_lon": 31.3042},
        {"stop_id": "L1_S29", "stop_name": "Hadayeq El Zaitoun", "stop_lat": 30.1057, "stop_lon": 31.3107},
        {"stop_id": "L1_S30", "stop_name": "Helmeyet El Zaitoun", "stop_lat": 30.1138, "stop_lon": 31.3142},
        {"stop_id": "L1_S31", "stop_name": "El Matareyya", "stop_lat": 30.1213, "stop_lon": 31.3176},
        {"stop_id": "L1_S32", "stop_name": "Ain Shams", "stop_lat": 30.1312, "stop_lon": 31.3190},
        {"stop_id": "L1_S33", "stop_name": "Ezbet El Nakhl", "stop_lat": 30.1394, "stop_lon": 31.3242},
        {"stop_id": "L1_S34", "stop_name": "El Marg", "stop_lat": 30.1521, "stop_lon": 31.3367},
        {"stop_id": "L1_S35", "stop_name": "New El Marg", "stop_lat": 30.1643, "stop_lon": 31.3380},
    ],
    "L2": [
        {"stop_id": "L2_S01", "stop_name": "Shobra El Kheima", "stop_lat": 30.1285, "stop_lon": 31.2442},
        {"stop_id": "L2_S02", "stop_name": "Kolleyyet El Zeraa", "stop_lat": 30.1189, "stop_lon": 31.2485},
        {"stop_id": "L2_S03", "stop_name": "Mezallat", "stop_lat": 30.1043, "stop_lon": 31.2459},
        {"stop_id": "L2_S04", "stop_name": "Khalafawy", "stop_lat": 30.0978, "stop_lon": 31.2443},
        {"stop_id": "L2_S05", "stop_name": "St. Teresa", "stop_lat": 30.0880, "stop_lon": 31.2453},
        {"stop_id": "L2_S06", "stop_name": "Road El Farag", "stop_lat": 30.0807, "stop_lon": 31.2452},
        {"stop_id": "L2_S07", "stop_name": "Masarra", "stop_lat": 30.0712, "stop_lon": 31.2456},
        {"stop_id": "L2_S08", "stop_name": "Al Shohadaa", "stop_lat": 30.0611, "stop_lon": 31.2458},  # Transfer
        {"stop_id": "L2_S09", "stop_name": "Attaba", "stop_lat": 30.0524, "stop_lon": 31.2465},
        {"stop_id": "L2_S10", "stop_name": "Mohamed Naguib", "stop_lat": 30.0453, "stop_lon": 31.2439},
        {"stop_id": "L2_S11", "stop_name": "Sadat", "stop_lat": 30.0442, "stop_lon": 31.2347},  # Transfer
        {"stop_id": "L2_S12", "stop_name": "Opera", "stop_lat": 30.0419, "stop_lon": 31.2250},
        {"stop_id": "L2_S13", "stop_name": "Dokki", "stop_lat": 30.0383, "stop_lon": 31.2123},
        {"stop_id": "L2_S14", "stop_name": "Bohooth", "stop_lat": 30.0359, "stop_lon": 31.2015},
        {"stop_id": "L2_S15", "stop_name": "Cairo University", "stop_lat": 30.0260, "stop_lon": 31.2011},
        {"stop_id": "L2_S16", "stop_name": "Faisal", "stop_lat": 30.0172, "stop_lon": 31.2038},
        {"stop_id": "L2_S17", "stop_name": "Giza", "stop_lat": 30.0107, "stop_lon": 31.2066},
        {"stop_id": "L2_S18", "stop_name": "Omm El Misryeen", "stop_lat": 29.9877, "stop_lon": 31.2089},
        {"stop_id": "L2_S19", "stop_name": "Sakiat Mekki", "stop_lat": 29.9539, "stop_lon": 31.2085},
        {"stop_id": "L2_S20", "stop_name": "El Mounib", "stop_lat": 29.9813, "stop_lon": 31.2124},
    ],
    "L3": [
        {"stop_id": "L3_S01", "stop_name": "Adly Mansour", "stop_lat": 30.1472, "stop_lon": 31.4214},
        {"stop_id": "L3_S02", "stop_name": "Hikestep", "stop_lat": 30.1437, "stop_lon": 31.4051},
        {"stop_id": "L3_S03", "stop_name": "Omar Ibn El Khattab", "stop_lat": 30.1400, "stop_lon": 31.3944},
        {"stop_id": "L3_S04", "stop_name": "Qobaa", "stop_lat": 30.1348, "stop_lon": 31.3836},
        {"stop_id": "L3_S05", "stop_name": "Hesham Barakat", "stop_lat": 30.1309, "stop_lon": 31.3730},
        {"stop_id": "L3_S06", "stop_name": "El Nozha", "stop_lat": 30.1279, "stop_lon": 31.3604},
        {"stop_id": "L3_S07", "stop_name": "Nadi El Shams", "stop_lat": 30.1213, "stop_lon": 31.3451},
        {"stop_id": "L3_S08", "stop_name": "Alf Maskan", "stop_lat": 30.1190, "stop_lon": 31.3398},
        {"stop_id": "L3_S09", "stop_name": "Heliopolis", "stop_lat": 30.1088, "stop_lon": 31.3381},
        {"stop_id": "L3_S10", "stop_name": "Haroun", "stop_lat": 30.1014, "stop_lon": 31.3330},
        {"stop_id": "L3_S11", "stop_name": "Al Ahram", "stop_lat": 30.0916, "stop_lon": 31.3263},
        {"stop_id": "L3_S12", "stop_name": "Koleyet El Banat", "stop_lat": 30.0840, "stop_lon": 31.3284},
        {"stop_id": "L3_S13", "stop_name": "Stadium", "stop_lat": 30.0730, "stop_lon": 31.3173},
        {"stop_id": "L3_S14", "stop_name": "Fair Zone", "stop_lat": 30.0733, "stop_lon": 31.3009},
        {"stop_id": "L3_S15", "stop_name": "Abbassiya", "stop_lat": 30.0722, "stop_lon": 31.2838},
        {"stop_id": "L3_S16", "stop_name": "Abdou Pasha", "stop_lat": 30.0644, "stop_lon": 31.2752},
        {"stop_id": "L3_S17", "stop_name": "El Geish", "stop_lat": 30.0614, "stop_lon": 31.2673},
        {"stop_id": "L3_S18", "stop_name": "Bab El Shaaria", "stop_lat": 30.0542, "stop_lon": 31.2558},
        {"stop_id": "L3_S19", "stop_name": "Attaba", "stop_lat": 30.0524, "stop_lon": 31.2465},
        {"stop_id": "L3_S20", "stop_name": "Nasser", "stop_lat": 30.0535, "stop_lon": 31.2389},  # Transfer
        {"stop_id": "L3_S21", "stop_name": "Maspero", "stop_lat": 30.0561, "stop_lon": 31.2321},
        {"stop_id": "L3_S22", "stop_name": "Safaa Hegazy", "stop_lat": 30.0597, "stop_lon": 31.2241},
        {"stop_id": "L3_S23", "stop_name": "Kit Kat", "stop_lat": 30.0664, "stop_lon": 31.2128},
        {"stop_id": "L3_S24", "stop_name": "Sudan", "stop_lat": 30.0702, "stop_lon": 31.2046},
        {"stop_id": "L3_S25", "stop_name": "Imbaba", "stop_lat": 30.0762, "stop_lon": 31.2074},
    ],
}

# Service types (weekday, weekend, holidays)
SERVICE_IDS = ["weekday", "saturday", "sunday"]

# Trip directions
DIRECTIONS = [0, 1]  # 0 = outbound, 1 = inbound


def generate_trip_data(num_trips: int = 100) -> int:
    """Generate mock GTFS trip data and write to NDJSON file."""
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    
    written = 0
    generated_at = datetime.now(timezone.utc).isoformat()
    
    with OUT_FILE.open("w", encoding="utf8") as fh:
        for i in range(num_trips):
            # Pick random route
            route = random.choice(ROUTES)
            route_id = route["route_id"]
            
            # Pick random direction
            direction_id = random.choice(DIRECTIONS)
            
            # Pick random service (mostly weekdays)
            service_id = random.choices(SERVICE_IDS, weights=[0.7, 0.15, 0.15])[0]
            
            # Generate trip_id
            trip_id = f"trip_{route_id}_{direction_id}_{i}"
            
            # Pick random start stop
            stops_for_route = STOPS[route_id]
            if direction_id == 1:  # Reverse for inbound
                stops_for_route = list(reversed(stops_for_route))
            
            start_stop_idx = random.randint(0, len(stops_for_route) - 3)
            end_stop_idx = random.randint(start_stop_idx + 2, len(stops_for_route) - 1)
            
            origin_stop = stops_for_route[start_stop_idx]
            destination_stop = stops_for_route[end_stop_idx]
            
            # Generate realistic trip time (between 5 AM and 11 PM)
            hour = random.randint(5, 23)
            minute = random.choice([0, 15, 30, 45])
            departure_time = time(hour, minute)
            
            # Calculate arrival time (2-5 minutes per stop)
            num_stops = end_stop_idx - start_stop_idx + 1
            travel_minutes = num_stops * random.randint(2, 5)
            arrival_datetime = datetime.combine(datetime.today(), departure_time) + timedelta(minutes=travel_minutes)
            arrival_time = arrival_datetime.time()
            
            # Ridership (random but realistic)
            ridership = random.randint(50, 800)
            
            # On-time performance (mostly on time)
            delay_minutes = random.choices([0, 1, 2, 3, 5, 10, 15], weights=[0.5, 0.2, 0.15, 0.08, 0.04, 0.02, 0.01])[0]
            
            # Trip date (within last 30 days)
            days_ago = random.randint(0, 30)
            trip_date = (datetime.now() - timedelta(days=days_ago)).date().isoformat()
            
            record = {
                "trip_id": trip_id,
                "route_id": route_id,
                "route_short_name": route["route_short_name"],
                "route_long_name": route["route_long_name"],
                "route_type": route["route_type"],  # 1 = Metro/Subway
                "route_color": route["route_color"],
                "direction_id": direction_id,
                "direction_name": "Outbound" if direction_id == 0 else "Inbound",
                "service_id": service_id,
                "trip_date": trip_date,
                "departure_time": departure_time.strftime("%H:%M:%S"),
                "arrival_time": arrival_time.strftime("%H:%M:%S"),
                "origin_stop_id": origin_stop["stop_id"],
                "origin_stop_name": origin_stop["stop_name"],
                "origin_lat": origin_stop["stop_lat"],
                "origin_lon": origin_stop["stop_lon"],
                "destination_stop_id": destination_stop["stop_id"],
                "destination_stop_name": destination_stop["stop_name"],
                "destination_lat": destination_stop["stop_lat"],
                "destination_lon": destination_stop["stop_lon"],
                "num_stops": num_stops,
                "ridership": ridership,
                "delay_minutes": delay_minutes,
                "on_time": delay_minutes <= 2,
                "generated_at": generated_at,
            }
            
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")
            written += 1
    
    return written


def main():
    parser = argparse.ArgumentParser(description="Generate mock GTFS transit data for testing")
    parser.add_argument("--trips", type=int, default=100, help="Number of trip records to generate")
    args = parser.parse_args()
    
    print(f"Generating {args.trips} mock GTFS trip records (Cairo Metro)...")
    n = generate_trip_data(args.trips)
    print(f"✓ Wrote {n} trip records to {OUT_FILE}")
    print(f"  Routes: Line 1 (Red), Line 2 (Yellow), Line 3 (Green)")
    print(f"  (Mock data for Cairo Metro - 3 lines, 80+ stations)")


if __name__ == "__main__":
    main()
