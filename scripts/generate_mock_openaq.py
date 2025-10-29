"""Mock OpenAQ data generator for testing

Generates realistic mock air quality data for Cairo, Egypt when the OpenAQ API is unavailable.
Creates NDJSON file at `data/openaq_data.ndjson`.

Usage:
    python scripts/generate_mock_openaq.py --records 100
"""
import argparse
import json
import random
from datetime import datetime, timezone, timedelta
from pathlib import Path

OUT_DIR = Path("data")
OUT_FILE = OUT_DIR / "openaq_data.ndjson"

# Cairo monitoring locations
LOCATIONS = [
    "US Diplomatic Post: Cairo",
    "Cairo - Manshiyat Naser",
    "Cairo - Maadi",
    "Cairo - Nasr City",
    "Cairo - Heliopolis",
]

# Air quality parameters with realistic ranges for Cairo
PARAMETERS = {
    "pm25": {"unit": "µg/m³", "min": 20, "max": 250},  # PM2.5
    "pm10": {"unit": "µg/m³", "min": 40, "max": 400},  # PM10
    "o3": {"unit": "µg/m³", "min": 10, "max": 180},    # Ozone
    "no2": {"unit": "µg/m³", "min": 15, "max": 200},   # Nitrogen Dioxide
    "so2": {"unit": "µg/m³", "min": 5, "max": 80},     # Sulfur Dioxide
    "co": {"unit": "ppm", "min": 0.2, "max": 5.0},     # Carbon Monoxide
}

# Approximate Cairo coordinates
CAIRO_COORDS = {
    "lat": 30.0444,
    "lon": 31.2357,
}


def generate_mock_data(num_records: int = 100) -> int:
    """Generate mock OpenAQ data and write to NDJSON file."""
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    
    written = 0
    fetched_at = datetime.now(timezone.utc).isoformat()
    
    with OUT_FILE.open("w", encoding="utf8") as fh:
        for i in range(num_records):
            # Pick random location
            location = random.choice(LOCATIONS)
            
            # Pick random parameter
            param_name = random.choice(list(PARAMETERS.keys()))
            param_info = PARAMETERS[param_name]
            
            # Generate realistic value with some variation
            value = round(random.uniform(param_info["min"], param_info["max"]), 2)
            
            # Add small random coordinate offset for each location
            latitude = CAIRO_COORDS["lat"] + random.uniform(-0.1, 0.1)
            longitude = CAIRO_COORDS["lon"] + random.uniform(-0.1, 0.1)
            
            # Generate timestamp (recent readings within last 24 hours)
            hours_ago = random.randint(0, 24)
            date_utc = (datetime.now(timezone.utc) - timedelta(hours=hours_ago)).isoformat()
            
            record = {
                "measurement_id": f"mock_{i}_{param_name}",
                "location": location,
                "city": "Cairo",
                "country": "EG",
                "parameter": param_name,
                "value": value,
                "unit": param_info["unit"],
                "latitude": round(latitude, 6),
                "longitude": round(longitude, 6),
                "date_utc": date_utc,
                "fetched_at": fetched_at,
            }
            
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")
            written += 1
    
    return written


def main():
    parser = argparse.ArgumentParser(description="Generate mock OpenAQ data for testing")
    parser.add_argument("--records", type=int, default=100, help="Number of records to generate")
    args = parser.parse_args()
    
    print(f"Generating {args.records} mock OpenAQ records...")
    n = generate_mock_data(args.records)
    print(f"✓ Wrote {n} mock measurements to {OUT_FILE}")
    print(f"  (Created for testing when OpenAQ API is unavailable)")


if __name__ == "__main__":
    main()
