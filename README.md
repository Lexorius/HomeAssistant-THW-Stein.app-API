
# THW Stein – Home Assistant Custom Integration (HACS)
[release-url]: https://github.com/Lexorius/HomeAssistant-THW-Stein.app-API/releases
[release-badge]: https://img.shields.io/github/v/release/Lexorius/HomeAssistant-THW-Stein.app-APIy?style=flat-square

# Info: Dies ist ein Privates Projekt. Es hat nichts mit dem THW zu tun.

# Benutzung auf eigene Verantwortung. 

Displays vehicle and asset status from **Stein.APP** directly in Home Assistant.

**Version 0.3.6** – 2025-07-04 

---

## Features
* Bearer‑Token authentication (only *API‑Key* required)
* Uses **BU‑ID** to address your organisation unit
* Polls `/assets/?buIds=<BU-ID>` and creates one sensor per asset
* Sensor state = operational status (`Einsatzbereit`, `Im Einsatz`, …)
* Rich attributes: `label`, `comment`, `category`, `last_modified`, …

---

## Installation
### via HACS
1. Add this repo (`https://github.com/Lexorius/HomeAssistant-THW-Stein.app-API`) as **custom repository** (type *Integration*).
2. Install **THW Stein**.
3. Restart Home Assistant.

### Manual
1. Copy the folder `custom_components/thw_stein` into your HA `config/custom_components/`.
2. Copy `hacs.json` and `icon.png` to repo root if you want HACS discovery.
3. Restart Home Assistant.

---

## Configuration
| Field | Description |
|-------|-------------|
| **API‑Key** | Your Bearer token from Stein.APP |
| **BU‑ID**  | Numeric ID of your organisation unit |
| **Scan‑Intervall** | Poll frequency in seconds (default 300) |

---

## Sensor Naming
`<Label> <Name> <RadioName>` – combined and cleaned.

Example: `FGr Kommunikation` → **State**: `Einsatzbereit`

---

## Endpoints Used
* `GET https://stein.app/api/api/ext/assets/?buIds=<BU-ID>` – list
* `GET https://stein.app/api/api/ext/assets/<asset_id>` – detail (reserved for future attributes)

---
