# E-Bike Ladestationen Deutschland

Fragt wöchentlich per [Overpass API](https://overpass-api.de/) alle E-Bike- und Fahrrad-Ladestationen in Deutschland ab und stellt das Ergebnis als JSON über GitHub Pages bereit.

## Download

Die aktuelle JSON-Datei ist über GitHub Pages verfügbar:

**<https://ratopi.github.io/ebike-ladestationen/ebike_charging_stations.json>**

## JSON-Format

```json
{
  "generated": "2026-04-22T03:00:00+00:00",
  "count": 1234,
  "stations": [
    {
      "lat": 51.123,
      "lon": 7.456,
      "name": "Ladestation am Markt",
      "operator": "Stadtwerke",
      "capacity": 4,
      "socket_types": ["schuko", "type2"],
      "osm_id": 12345678
    }
  ]
}
```

## Lokal ausführen

```bash
pip install -r requirements.txt
python fetch_stations.py
```

## GitHub Actions

Der Workflow `.github/workflows/ebike-ladestationen.yml` läuft jeden Montag um 03:00 UTC und pusht die JSON-Datei in einen `gh-pages`-Branch (ohne History).

Unter **Settings → Pages** den Branch `gh-pages` als Quelle auswählen.

