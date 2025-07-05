"""Sensors for THW Stein assets."""
from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .api import SteinClient

STATUS_MAP = {
    "ready": "Einsatzbereit",
    "inuse": "Im Einsatz",
    "maint": "In Wartung",
    "semiready": "Bedingt einsatzbereit",
    "notready": "Nicht einsatzbereit",
}

EINSATZVORBEHALT = {
    "true": "Fahrzeug ist unter Einsatzvorbehalt",
    "false": ' ',
}

async def async_setup_entry(hass, entry, async_add_entities):
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]
    client: SteinClient = data["client"]

    entities = [SteinAssetSensor(coordinator, client, asset) for asset in coordinator.data]
    async_add_entities(entities, update_before_add=True)

class SteinAssetSensor(CoordinatorEntity, SensorEntity):
    _attr_has_entity_name = True

    def __init__(self, coordinator, client: SteinClient, asset):
        super().__init__(coordinator)
        self._client = client
        self._asset_id = asset["id"]
        self._update_from_asset(asset)

    @staticmethod
    def _compose_name(asset) -> str:
        parts = [asset.get("label")]
        if asset.get("radioName"):
            parts.append(' - ')
            parts.append(asset["radioName"])
        if asset.get("name"):
            parts.append(' - ')
            parts.append(asset["name"])

        if asset.get("category"):
            parts.append(' - ')
            parts.append(asset["category"])            
        return " ".join(filter(None, parts))

    def _update_from_asset(self, asset):
        slug = self._compose_name(asset).lower().replace(" ", "_").replace("/", "_")
        self._attr_unique_id = f"stein_app_{self._asset_id}"
        #self._attr_name = f"stein_app_{slug}" 
        #self._attr_unique_id = f"stein_{self._asset_id}"
        self._attr_name = self._compose_name(asset)
        raw_status = asset.get("status")
        raw_einsatzvorbehalt = asset.get("operationReservation")
        self._attr_native_value = STATUS_MAP.get(raw_status)
        self._attr_extra_state_attributes = {
            "name": asset.get("name"),
            "label": asset.get("label"),
            "id": asset.get("id"),
            "status": STATUS_MAP.get(raw_status),
            "comment": asset.get("comment"),
            "category": asset.get("category"),
            "last_modified": asset.get("lastModified"),
            "last_modified_by": asset.get("lastModifiedBy"),
            "bu_id": asset.get("buId"),
            "group_id": asset.get("groupId"),
            "radioName": asset.get("radioName"),
            "issi": asset.get("issi"),
            "operationReservation": asset.get("operationReservation"),                              
            "operationReservationText": EINSATZVORBEHALT.get(raw_einsatzvorbehalt),    
        }

#//  "buId": 0,
#//  "groupId": 0,
#//  "id": 0,
#//  "label": "",
#//  "name": "string",
#//  "status": "ready",
#//  "comment": "string",
#//  "category": "string",
#//  "deleted": false,
#//  "lastModified": "2019-08-24T14:15:22Z",
#//  "created": "2019-08-24T14:15:22Z",
#//  "lastModifiedBy": "string",
#//  "radioName": "string",
#//  "issi": "string",
#//  "sortOrder": 0,
#//  "operationReservation": false    

    async def _handle_coordinator_update(self):
        for asset in self.coordinator.data:
            if asset["id"] == self._asset_id:
                self._update_from_asset(asset)
                break
        await super()._handle_coordinator_update()
