"""Config flow for THW Stein (API-Key and BU-ID)."""
from __future__ import annotations
import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN, CONF_API_KEY, CONF_BU_ID, CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL

DATA_SCHEMA = vol.Schema({
    vol.Required(CONF_API_KEY): str,
    vol.Required(CONF_BU_ID): int,
    vol.Optional(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): vol.All(vol.Coerce(int), vol.Range(min=60, max=3600)),
})

class SteinConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="THW Stein", data=user_input)
        return self.async_show_form(step_id="user", data_schema=DATA_SCHEMA)
