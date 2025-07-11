# THW Stein – Home Assistant Custom Integration (HACS)


[![GitHub Release](https://img.shields.io/github/v/release/Lexorius/HomeAssistant-THW-Stein.app-API?sort=semver&style=for-the-badge&color=green)](https://github.com/Lexorius/HomeAssistant-THW-Stein.app-API/releases)
[![GitHub Release Date](https://img.shields.io/github/release-date/Lexorius/HomeAssistant-THW-Stein.app-API?style=for-the-badge&color=green)](https://github.com/Lexorius/HomeAssistant-THW-Stein.app-API/releases)
![GitHub Downloads (all assets, latest release)](https://img.shields.io/github/downloads/Lexorius/HomeAssistant-THW-Stein.app-API/latest/total?style=for-the-badge&label=Downloads%20latest%20Release)
![HA Analytics](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fanalytics.home-assistant.io%2Fcustom_integrations.json&query=%.total&style=for-the-badge&label=Active%20Installations&color=red)
[![hacs](https://img.shields.io/badge/HACS-Integration-blue.svg?style=for-the-badge)](https://github.com/hacs/integration)


## Overview

![](icon.png)
# Info: Dies ist ein Privates Projekt. Es hat nichts mit dem THW zu tun.

# Benutzung auf eigene Verantwortung. 

Displays vehicle and asset status from **Stein.APP** directly in Home Assistant.

**Version 0.4.0** – 2025-07-04 

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
