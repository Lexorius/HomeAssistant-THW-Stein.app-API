# THW Stein – Home Assistant Custom Integration

Integration zur Anzeige von Assets/Fahrzeugen aus der Stein.APP im Home Assistant.

## Version 0.2.5

- Umstellung auf Bearer-Token-Authentifizierung
- Nutzung der `bu_id` direkt statt OV-Namen
- Zugriff über API: `/assets/?buIds=…` und `/assets/<id>`

## Einrichtung

Füge die Integration über HACS oder manuell ein.
Konfiguriert wird:

- API-Key (Bearer Token)
- BU-ID (numerisch)

## Quelle

Basierend auf der API von [steinapi](https://github.com/oscarminus/steinapi)
