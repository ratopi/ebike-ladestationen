#!/usr/bin/env python3
"""Fetch e-bike/bicycle charging stations in Germany via Overpass API."""

import json
import requests
from datetime import datetime, timezone

OVERPASS_URL = "https://overpass-api.de/api/interpreter"

QUERY = """
[out:json][timeout:120];
area["ISO3166-1"="DE"]->.germany;
(
  node["amenity"="charging_station"]["bicycle"="yes"](area.germany);
  way["amenity"="charging_station"]["bicycle"="yes"](area.germany);
  node["amenity"="bicycle_charging_station"](area.germany);
  way["amenity"="bicycle_charging_station"](area.germany);
);
out center tags;
"""


def fetch():
    print("Querying Overpass API...")
    resp = requests.post(
        OVERPASS_URL,
        data={"data": QUERY},
        headers={"User-Agent": "ebike-ladestationen/1.0", "Accept": "*/*"},
        timeout=180,
    )
    resp.raise_for_status()
    data = resp.json()

    stations = []
    for el in data.get("elements", []):
        tags = el.get("tags", {})
        lat = el.get("lat") or el.get("center", {}).get("lat")
        lon = el.get("lon") or el.get("center", {}).get("lon")
        if lat is None or lon is None:
            continue

        # Extract socket types (only direct "socket:<type>" keys, not sub-keys like "socket:schuko:voltage")
        socket_types = []
        for key, val in tags.items():
            if key.startswith("socket:") and key.count(":") == 1:
                socket_types.append(key.split(":")[1])

        # If no explicit socket tags, check for general plug info
        if not socket_types and tags.get("bicycle:plug"):
            socket_types.append(tags["bicycle:plug"])

        capacity = tags.get("capacity", tags.get("bicycle:capacity"))
        try:
            capacity = int(capacity) if capacity else None
        except (ValueError, TypeError):
            capacity = None

        stations.append({
            "lat": lat,
            "lon": lon,
            "name": tags.get("name"),
            "operator": tags.get("operator"),
            "capacity": capacity,
            "socket_types": socket_types,
            "osm_id": el.get("id"),
        })

    result = {
        "generated": datetime.now(timezone.utc).isoformat(),
        "count": len(stations),
        "stations": stations,
    }

    with open("ebike_charging_stations.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"Done. {len(stations)} stations written to ebike_charging_stations.json")


if __name__ == "__main__":
    fetch()

