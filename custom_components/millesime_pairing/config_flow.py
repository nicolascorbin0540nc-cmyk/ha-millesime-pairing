from homeassistant import config_entries
from homeassistant.core import callback
import voluptuous as vol

DOMAIN = "millesime_pairing"

class MillesimePairingConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        if user_input is not None:
            return self.async_create_entry(title="Millésime & Accords Vins (Test Lab)", data={})

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({})
        )
