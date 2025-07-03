"""Home Assistant sensor platform for THW Stein assets."""
from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

# Map Stein status strings → human‑friendly German labels
STATUS_MAP = {
    "ready": "Einsatzbereit",
    "semiready": "Bedingt einsatzbereit",
    "notready": "Nicht einsatzbereit",
    "inuse": "Im Einsatz",
    "maint": "In Wartung",
}


async def async_setup_entry(hass, entry, async_add_entities):
    """Create sensor entities after config entry is set up."""
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]

    entities = [SteinAssetSensor(coordinator, entry, asset) for asset in coordinator.data]
    async_add_entities(entities)


class SteinAssetSensor(CoordinatorEntity, SensorEntity):
    """Represents a single Stein asset as a sensor in Home Assistant."""

    _attr_has_entity_name = True

    def __init__(self, coordinator, entry, asset):
        super().__init__(coordinator)
        self._entry = entry
        self._id = asset["id"]
        self._update_from_asset(asset)

    # ------------------------------------------------------------------ #
    # Helpers
    # ------------------------------------------------------------------ #
    def _update_from_asset(self, asset):
        """Populate attributes from a Stein asset dict."""
        self._attr_unique_id = f"{self._entry.entry_id}_{self._id}"
        self._attr_name = asset.get("label")
        self._attr_icon = (
            "mdi:truck"
            if str(asset.get("category", "")).lower().startswith("f")
            else "mdi:package-variant"
        )
        self._attr_state = STATUS_MAP.get(asset.get("status"), asset.get("status"))
        self._attr_extra_state_attributes = {
            "plate": asset.get("plate"),
            "category": asset.get("category"),
            "last_modified": asset.get("lastModified"),
        }

    # ------------------------------------------------------------------ #
    # HA callbacks
    # ------------------------------------------------------------------ #
    async def _handle_coordinator_update(self):
        for asset in self.coordinator.data:
            if asset["id"] == self._id:
                self._update_from_asset(asset)
                break
        await super()._handle_coordinator_update()
