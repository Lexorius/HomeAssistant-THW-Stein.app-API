from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .api import STATUS_MAP
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]
    async_add_entities([
        SteinAssetSensor(coordinator, entry, asset) for asset in coordinator.data
    ])

class SteinAssetSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, entry, asset):
        super().__init__(coordinator)
        self._entry, self._id = entry, asset["id"]
        self._update(asset)

    def _update(self, asset):
        self._attr_unique_id = f"{self._entry.entry_id}_{self._id}"
        self._attr_name = asset["label"]
        self._attr_icon = "mdi:truck" if asset["category"].lower().startswith("f") else "mdi:package-variant"
        self._attr_state = STATUS_MAP.get(asset["status"], asset["status"])
        self._attr_extra_state_attributes = {
            "plate": asset.get("plate"),
            "category": asset.get("category"),
            "last_modified": asset.get("lastModified"),
        }

    async def _handle_coordinator_update(self):
        for a in self.coordinator.data:
            if a["id"] == self._id:
                self._update(a)
                break
        await super()._handle_coordinator_update()