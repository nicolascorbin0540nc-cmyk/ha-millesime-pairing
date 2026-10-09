import os
import logging
from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant, callback
from .pairer import WinePairer

DOMAIN = "millesime_pairing"
_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry, async_add_entities):
    db_path = os.path.join(os.path.dirname(__file__), "pairings_db.json")
    pairer = WinePairer(db_path)

    pairing_sensor = WinePairingTestSensor(pairer)
    async_add_entities([pairing_sensor])

    @callback
    def handle_search_event(event):
        dish = event.data.get("dish", "")
        pairing_sensor.update_pairing(dish)

    hass.bus.async_listen(f"{DOMAIN}_search_pairing", handle_search_event)


class WinePairingTestSensor(SensorEntity):
    def __init__(self, pairer: WinePairer):
        self._pairer = pairer
        self._attr_name = "Recommandation Accord Vin (Test)"
        self._attr_unique_id = "millesime_pairing_wine_pairing"
        self._attr_icon = "mdi:glass-wine"
        self._state = "Aucune recherche"
        self._attr_extra_state_attributes = {
            "plat": "",
            "vins_recommandes": [],
            "conseil": ""
        }

    @property
    def state(self):
        return self._state

    def update_pairing(self, dish: str):
        if not dish:
            return
        result = self._pairer.find_pairing(dish)
        if result["wines"]:
            self._state = ", ".join(result["wines"][:2])
        else:
            self._state = "Pas de recommandation"

        self._attr_extra_state_attributes = {
            "plat": dish,
            "vins_recommandes": result["wines"],
            "conseil": result["advice"]
        }
        self.async_write_ha_state()
