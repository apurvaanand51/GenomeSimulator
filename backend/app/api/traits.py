from __future__ import annotations

from app.core.config import DATA_DIR
import json


def load_traits() -> list[dict]:
    with open(DATA_DIR / "traits" / "traits.json", "r", encoding="utf-8") as handle:
        return json.load(handle)
