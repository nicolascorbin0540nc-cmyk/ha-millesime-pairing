import os
import logging
from homeassistant.core import HomeAssistant, ServiceCall, ServiceResponse, SupportsResponse
from homeassistant.config_entries import ConfigEntry

from .pairer import WinePairer

DOMAIN = "millesime_pairing"
PLATFORMS = ["sensor"]
_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    db_path = os.path.join(os.path.dirname(__file__), "pairings_db.json")
    pairer = WinePairer(db_path)

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    async def handle_get_pairing(call: ServiceCall) -> ServiceResponse:
        dish = call.data.get("dish", "")
        result = pairer.find_pairing(dish)
        
        hass.bus.async_fire(f"{DOMAIN}_search_pairing", {"dish": dish})

        return {
            "dish": dish,
            "recommended_wines": result["wines"],
            "advice": result["advice"],
            "matched_keyword": result["matched_keyword"]
        }

    hass.services.async_register(
        DOMAIN,
        "get_pairing",
        handle_get_pairing,
        supports_response=SupportsResponse.ONLY
    )

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
