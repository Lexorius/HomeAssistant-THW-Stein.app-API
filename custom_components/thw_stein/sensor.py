"""Sensors for THW Stein assets.

Erzeugt:
* pro Asset einen Sensor mit Status & Attributen
* State = übersetzter Status (+ Zusatz „Unter Einsatzvorbehalt“)
* Entity-ID beginnt mit stein_app_<asset_id>
"""
from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .api import SteinClient

# ------------------------- Übersetzungen ------------------------- #
# Roh-Status   → Anzeige im Frontend
STATUS_MAP = {
    "ready": "Einsatzbereit",
    "inuse": "Im Einsatz",
    "maint": "In Wartung",
    "semiready": "Bedingt einsatzbereit",
    "notready": "Nicht einsatzbereit",
}

# Zusatztext, falls operationReservation==true
EINSATZVORBEHALT = {
    True:  "Fahrzeug ist unter Einsatzvorbehalt",
    False: "",
}

# -------------------- Setup durch HA ----------------------------- #
async def async_setup_entry(hass, entry, async_add_entities):
    """Wird von Home Assistant beim Laden der Integration aufgerufen."""
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]          # liefert periodisch Asset-Liste
    client: SteinClient = data["client"]       # aktuell ungenutzt – Reserve

    # Liste aller Sensor-Objekte erzeugen
    entities = [
        SteinAssetSensor(coordinator, client, asset)
        for asset in coordinator.data
    ]
    async_add_entities(entities, update_before_add=True)


# ----------------------------------------------------------------- #
# Sensor-Klasse  (ein Sensor = ein Asset)
# ----------------------------------------------------------------- #
class SteinAssetSensor(CoordinatorEntity, SensorEntity):
    """Ein Sensor repräsentiert genau EIN Asset."""
    _attr_has_entity_name = True  # neue HA-Option: kein doppelter Name nötig

    def __init__(self, coordinator, client: SteinClient, asset):
        """Speichert Asset-ID & legt Initialwerte an."""
        super().__init__(coordinator)
        self._client = client          # für mögliche Detail-Abrufe
        self._asset_id = asset["id"]   # eindeutige ID aus JSON
        self._update_from_asset(asset) # Initial-Daten setzen

    # ---------- Hilfsfunktion: Anzeigename zusammensetzen ---------- #
    @staticmethod
    def _compose_name(asset) -> str:
        """Label, RadioName & Name in einer Zeile zusammenführen."""
        parts = [asset.get("label")]          # z. B. „FGr Kommunikation“
        if asset.get("radioName"):            # Funkrufname?
            parts.append("-")
            parts.append(asset["radioName"])
        if asset.get("name"):                 # Freitext Name?
            parts.append("-")
            parts.append(asset["name"])
        if asset.get("category"):             # Kategorie (z. B. K (A))
            parts.append("-")
            parts.append(asset["category"])
        return " ".join(filter(None, parts))

    # -------------- Daten aus Asset-Dict → Entity ------------------ #
    def _update_from_asset(self, asset):
        """Aktualisiere State & Attribute aus JSON."""
        # Entity-ID: einzigartig & stabil
        self._attr_unique_id = f"stein_app_{self._asset_id}"

        # Anzeigename (im UI) – nicht die Entity-ID!
        self._attr_name = self._compose_name(asset)

        # ----- State (native_value) -------------------------------- #
        raw_status = asset.get("status")                # z. B. "ready"
        status_text = STATUS_MAP.get(raw_status, raw_status)

        # Einsatzvorbehalt als Zusatz
        if asset.get("operationReservation"):
            status_text += " (Unter Einsatzvorbehalt)"
        self._attr_native_value = status_text

        # ----- Attribute (werden im Entwickler-Tool angezeigt) ----- #
        self._attr_extra_state_attributes = {
            "id": asset.get("id"),
            "label": asset.get("label"),
            "name": asset.get("name"),
            "radio_name": asset.get("radioName"),
            "category": asset.get("category"),
            "status_raw": raw_status,
            "comment": asset.get("comment"),
            "last_modified": asset.get("lastModified"),
            "last_modified_by": asset.get("lastModifiedBy"),
            "bu_id": asset.get("buId"),
            "group_id": asset.get("groupId"),
            "issi": asset.get("issi"),
            "huValidUntil": asset.get("huValidUntil"),
            "operation_reservation": asset.get("operationReservation"),
            "operation_reservation_text": EINSATZVORBEHALT[
                asset.get("operationReservation")
            ],
        }

    # -------- Callback: Coordinator liefert neue Asset-Liste ------- #
    def _handle_coordinator_update(self) -> None:
        """Wird vom Coordinator synchron aufgerufen, wenn neue Daten da sind."""
        for asset in self.coordinator.data:
            if asset["id"] == self._asset_id:
                self._update_from_asset(asset)  # Sensor updaten
                break
        self.async_write_ha_state()             # Werte an HA weitergeben
