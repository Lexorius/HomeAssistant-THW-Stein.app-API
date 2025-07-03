import logging
from aiohttp import ClientSession
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .api import SteinClient
from .const import DOMAIN, CONF_API_KEY, CONF_BU_ID

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    session = ClientSession()
    api_key = entry.data[CONF_API_KEY]
    bu_id = int(entry.data[CONF_BU_ID])
    client = SteinClient(bu_id=bu_id, api_key=api_key, session=session)
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = client
    return True
