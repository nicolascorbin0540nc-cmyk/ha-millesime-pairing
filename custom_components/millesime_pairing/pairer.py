import json
import os
import unicodedata

def normalize_text(text: str) -> str:
    text = text.lower()
    return "".join(
        c for c in unicodedata.normalize("NFD", text)
        if unicodedata.category(c) != "MN"
    )

class WinePairer:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._db = {}
        self.load_db()

    def load_db(self):
        if os.path.exists(self.db_path):
            with open(self.db_path, "r", encoding="utf-8") as f:
                self._db = json.load(f)

    def find_pairing(self, dish: str) -> dict:
        clean_dish = normalize_text(dish)
        for keyword, data in self._db.items():
            if keyword in clean_dish:
                return {
                    "matched_keyword": keyword,
                    "wines": data["vins"],
                    "advice": data["conseil"]
                }
        return {
            "matched_keyword": None,
            "wines": ["Vin rouge générique léger", "Vin blanc sec polyvalent"],
            "advice": f"Aucun accord spécifique trouvé pour '{dish}'. Optez pour un vin équilibré."
        }
