"""Config flow for THW Stein integration."""
from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback

from .const import (
    DOMAIN,
    CONF_USERNAME,
    CONF_PASSWORD,
    CONF_BUNAME,
    CONF_SCAN_INTERVAL,
    DEFAULT_SCAN_INTERVAL,
)

DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_USERNAME): str,
        vol.Required(CONF_PASSWORD): str,
        vol.Required(CONF_BUNAME): str,
        vol.Optional(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): vol.All(
            vol.Coerce(int), vol.Range(min=60, max=3600)
        ),
    }
)


class SteinConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for THW Stein."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title=user_input[CONF_BUNAME], data=user_input)
        return self.async_show_form(step_id="user", data_schema=DATA_SCHEMA)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return SteinOptionsFlow(config_entry)


class SteinOptionsFlow(config_entries.OptionsFlow):
    """Options flow – allows editing after initial setup."""

    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)
        return self.async_show_form(step_id="init", data_schema=DATA_SCHEMA)
