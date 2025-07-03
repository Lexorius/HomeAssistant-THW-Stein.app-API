from datetime import timedelta
import logging
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from .const import DOMAIN, DEFAULT_SCAN_INTERVAL
from .api import SteinClient, SteinError

_LOGGER = logging.getLogger(__name__)
PLATFORMS = ["sensor"]

async def async_setup(hass, config):
    return True

async def async_setup_entry(hass, entry):
    session = async_get_clientsession(hass)
    client = SteinClient(entry.data["buname"], session=session)
    await client.login(entry.data["username"], entry.data["password"])

    async def _update():
        try:
            return await client.async_get_assets()
        except SteinError as exc:
            raise UpdateFailed(exc) from exc

    coordinator = DataUpdateCoordinator(
        hass, _LOGGER, name="Stein assets",
        update_method=_update,
        update_interval=timedelta(seconds=entry.data.get("scan_interval", DEFAULT_SCAN_INTERVAL)),
    )
    await coordinator.async_config_entry_first_refresh()
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {"client": client, "coordinator": coordinator}
    hass.config_entries.async_setup_platforms(entry, PLATFORMS)
    return True
