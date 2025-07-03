from homeassistant import config_entries
import voluptuous as vol
from .const import DOMAIN, CONF_API_KEY, CONF_BU_ID

class SteinConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            return self.async_create_entry(title="THW Stein", data=user_input)

        data_schema = vol.Schema({
            vol.Required(CONF_API_KEY): str,
            vol.Required(CONF_BU_ID): int,
        })

        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )
