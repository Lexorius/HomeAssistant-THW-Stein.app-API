"""Sensors for THW Stein assets."""
from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .api import SteinClient

STATUS_MAP = {
    "ready": "Einsatzbereit",
    "semiready": "Bedingt einsatzbereit",
    "notready": "Nicht einsatzbereit",
    "inuse": "Im Einsatz",
    "maint": "In Wartung",
}

async def async_setup_entry(hass, entry, async_add_entities):
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]
    client: SteinClient = data["client"]

    entities = [SteinAssetSensor(coordinator, client, asset) for asset in coordinator.data]
    async_add_entities(entities)


class SteinAssetSensor(CoordinatorEntity, SensorEntity):
    _attr_has_entity_name = True

    def __init__(self, coordinator, client: SteinClient, asset):
        super().__init__(coordinator)
        self._client = client
        self._asset_id = asset["id"]
        self._update_from_asset(asset)

    def _update_from_asset(self, asset):
        self._attr_unique_id = f"stein_{self._asset_id}"
        self._attr_name = asset.get("label")
        self._attr_state = STATUS_MAP.get(asset.get("status"), asset.get("status"))
        self._attr_extra_state_attributes = {
            "category": asset.get("category"),
            "plate": asset.get("plate"),
            "last_modified": asset.get("lastModified"),
        }

    async def _handle_coordinator_update(self):
        for asset in self.coordinator.data:
            if asset["id"] == self._asset_id:
                self._update_from_asset(asset)
                break
        await super()._handle_coordinator_update()
