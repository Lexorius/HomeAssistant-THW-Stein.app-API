"""Sensors for THW Stein assets.

Erzeugt:
* pro Asset einen Sensor mit Status & Attributen
* State = übersetzter Status (+ Zusatz „Unter Einsatzvorbehalt")
* Entity-ID beginnt mit stein_app_<asset_id>
"""
from __future__ import annotations

from datetime import datetime, timezone
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
        parts = [asset.get("label")]          # z. B. „FGr Kommunikation"
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

    # ---------- Hilfsfunktion: HU-Restlaufzeit berechnen ---------- #
    @staticmethod
    def _calculate_hu_remaining_hours(hu_valid_until) -> int | None:
        """Berechnet die verbleibenden Stunden bis zum HU-Ablaufdatum.
        
        Args:
            hu_valid_until: ISO-8601 Datumsstring oder None
            
        Returns:
            Anzahl der verbleibenden Stunden als Integer oder None bei Fehler
        """
        if not hu_valid_until:
            return None
            
        try:
            # Parse das HU-Ablaufdatum (erwartet ISO-8601 Format)
            # Beispielformate: "2024-12-31T23:59:59Z" oder "2024-12-31"
            if 'T' in hu_valid_until:
                # Vollständiges ISO-8601 Format mit Zeit
                hu_date = datetime.fromisoformat(hu_valid_until.replace('Z', '+00:00'))
            else:
                # Nur Datum, füge Zeit hinzu (Ende des Tages)
                hu_date = datetime.fromisoformat(f"{hu_valid_until}T23:59:59+00:00")
            
            # Aktuelle Zeit (mit Zeitzone)
            now = datetime.now(timezone.utc)
            
            # Differenz berechnen
            time_delta = hu_date - now
            
            # In Stunden umrechnen (abrunden auf ganze Stunden)
            remaining_hours = int(time_delta.total_seconds() / 3600)
            
            # Negative Werte bedeuten abgelaufen
            return remaining_hours
            
        except (ValueError, TypeError) as e:
            # Bei Parsing-Fehlern None zurückgeben
            return None

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

        # HU-Restlaufzeit berechnen
        hu_valid_until = asset.get("huValidUntil")
        hu_remaining_hours = self._calculate_hu_remaining_hours(hu_valid_until)
        
        # HU-Status Text erstellen
        hu_status_text = None
        if hu_remaining_hours is not None:
            if hu_remaining_hours < 0:
                hu_status_text = f"HU abgelaufen seit {abs(hu_remaining_hours)} Stunden"
            elif hu_remaining_hours < 24:
                hu_status_text = f"HU läuft in {hu_remaining_hours} Stunden ab"
            elif hu_remaining_hours < 168:  # 7 Tage
                days = hu_remaining_hours // 24
                hours = hu_remaining_hours % 24
                hu_status_text = f"HU läuft in {days} Tagen und {hours} Stunden ab"
            else:
                days = hu_remaining_hours // 24
                hu_status_text = f"HU läuft in {days} Tagen ab"

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
            "huValidUntil": hu_valid_until,
            "hu_remaining_hours": hu_remaining_hours,
            "hu_status": hu_status_text,
            "operation_reservation": asset.get("operationReservation"),
            "operation_reservation_text": EINSATZVORBEHALT[
                asset.get("operationReservation", False)  # Default False für sicheren Zugriff
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