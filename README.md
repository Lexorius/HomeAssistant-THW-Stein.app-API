# THW Stein – Home Assistant Custom Integration (HACS)

*Display vehicle & asset status from THW Stein.APP directly in Home Assistant.*

> ⚠️ Diese Integration nutzt die **inoffizielle API** der THW Stein.APP. Dieses Projekt steht in **keiner offiziellen Verbindung zum THW**.

---

## Version 0.1.5 (Juli 2025)
Funktionsfähige, voll dokumentierte Version. Behebt alle bekannten Fehler, ergänzt vollständige Konfigurations-Oberfläche und unterstützt Optionen.

---

## Funktionen
- Automatische Anzeige aller Fahrzeuge und Assets einer Organisationseinheit (z. B. OV)
- Statusanzeige pro Entity: `Einsatzbereit`, `In Wartung`, `Nicht einsatzbereit`, ...
- Anzeige von Attributen wie Kennzeichen, Kategorie und letzte Änderung
- Einrichtung komplett über die Benutzeroberfläche (Config Flow)
- Unterstützt Anpassung des Scan-Intervalls

---

## Installation
### Variante A: HACS (empfohlen)
1. Füge dieses GitHub-Repo zu HACS als benutzerdefiniertes Repository hinzu:  
   `https://github.com/Lexorius/HomeAssistant-THW-Stein.app-API`
2. Suche in HACS nach "THW Stein" und installiere es.
3. Starte Home Assistant neu.
4. Füge die Integration über Einstellungen → Geräte & Dienste → „+“ hinzu.

### Variante B: Manuell
1. Lade das ZIP von [GitHub Releases](https://github.com/Lexorius/HomeAssistant-THW-Stein.app-API/releases).
2. Entpacke es nach `config/custom_components/thw_stein/`.
3. Starte Home Assistant neu.
4. Füge die Integration über die UI hinzu.

---

## Repository‑Struktur
```
.
├── README.md
├── CHANGELOG.md
├── hacs.json
├── icon.png
└── custom_components/
    └── thw_stein/
        ├── __init__.py
        ├── api.py
        ├── sensor.py
        ├── config_flow.py
        ├── const.py
        ├── manifest.json
        └── translations/
```

---

## Quellen
- [steinapi (Python API Connector)](https://github.com/oscarminus/steinapi)
- [stoned_hermine (Änderungs-Tracker für Stein.APP)](https://github.com/peacekiller/stoned_hermine)
- [DIVERA 24/7](https://www.divera247.de/) – externe Software zur Einsatzkoordination

---

## Lizenz
[MIT License](LICENSE)

© 2025 [@lexorius](https://github.com/lexorius)
