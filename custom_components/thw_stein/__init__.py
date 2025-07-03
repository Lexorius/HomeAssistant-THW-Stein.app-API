"""THW Stein – Home Assistant integration entry file."""
from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import (
    DOMAIN,
    DEFAULT_SCAN_INTERVAL,
    CONF_USERNAME,
    CONF_PASSWORD,
    CONF_BUNAME,
    CONF_SCAN_INTERVAL,
)
from .api import SteinClient, SteinError

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["sensor"]


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Minimal setup – UI configuration only."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up THW Stein from a config entry."""
    session = async_get_clientsession(hass)
    client = SteinClient(entry.data[CONF_BUNAME], session=session)

    # Login once
    await client.login(entry.data[CONF_USERNAME], entry.data[CONF_PASSWORD])

    async def _update():
        try:
            return await client.async_get_assets()
        except SteinError as exc:
            raise UpdateFailed(exc) from exc

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="Stein Assets",
        update_method=_update,
        update_interval=timedelta(seconds=entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)),
    )
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {
        "client": client,
        "coordinator": coordinator,
    }

    hass.config_entries.async_setup_platforms(entry, PLATFORMS)
    return True
