"""Config flow for THW Stein – API key only."""
from __future__ import annotations
import aiohttp, voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from .const import DOMAIN, CONF_API_KEY, CONF_BUNAME, CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
from .api import SteinClient, SteinError
from homeassistant.helpers.aiohttp_client import async_get_clientsession

DATA_SCHEMA = vol.Schema({
    vol.Required(CONF_API_KEY): str,
    vol.Required(CONF_BUNAME): str,
    vol.Optional(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): vol.All(vol.Coerce(int), vol.Range(min=60, max=3600)),
})

class SteinConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            # Validate API key
            session = async_get_clientsession(self.hass)
            client = SteinClient(user_input[CONF_BUNAME], api_key=user_input[CONF_API_KEY], session=session)
            try:
                await client.login()
            except SteinError:
                errors["base"] = "auth_failed"
            if not errors:
                return self.async_create_entry(title=user_input[CONF_BUNAME], data=user_input)
        return self.async_show_form(step_id="user", data_schema=DATA_SCHEMA, errors=errors)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return SteinOptionsFlow(config_entry)

class SteinOptionsFlow(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self._entry = config_entry
    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)
        return self.async_show_form(step_id="init", data_schema=DATA_SCHEMA)
