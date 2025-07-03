"""Integration setup for THW Stein."""
from __future__ import annotations
import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    DOMAIN,
    CONF_API_KEY,
    CONF_BU_ID,
    CONF_SCAN_INTERVAL,
    DEFAULT_SCAN_INTERVAL,
)
from .api import SteinClient, SteinError

_LOGGER = logging.getLogger(__name__)
PLATFORMS = ["sensor"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    api_key = entry.data[CONF_API_KEY]
    bu_id = int(entry.data[CONF_BU_ID])
    session = async_get_clientsession(hass)

    client = SteinClient(bu_id=bu_id, api_key=api_key, session=session)

    async def _async_update():
        try:
            return await client.async_get_assets()
        except SteinError as exc:
            raise UpdateFailed(exc) from exc

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="stein_assets",
        update_method=_async_update,
        update_interval=timedelta(
            seconds=entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
        ),
    )
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {
        "client": client,
        "coordinator": coordinator,
    }

    hass.config_entries.async_setup_platforms(entry, PLATFORMS)
    return True
