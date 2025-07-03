# Changelog – Version 0.0.3

Veröffentlicht: Juli 2025

## ✨ Neue Funktionen
- Erstes lauffähiges Release mit HACS-Unterstützung
- UI-Integration via `config_flow.py` (keine YAML nötig)
- Automatische Erkennung aller Fahrzeuge/Assets per API
- Übersetzung von Statuswerten in deutschsprachige Sensorzustände

## ⚙️ Technische Änderungen
- `manifest.json` aktualisiert (`config_flow: true`)
- `__init__.py`: `async_setup` hinzugefügt für UI-Kompatibilität
- `sensor.py`: Fahrzeugstatus als Entity in HA darstellbar
- `api.py`: einfache Authentifizierung + Asset-Abfrage
