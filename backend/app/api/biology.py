from __future__ import annotations

import json

from app.core.config import DATA_DIR


def load_pathways() -> list[dict]:
    with open(DATA_DIR / "pathways" / "pathways.json", "r", encoding="utf-8") as handle:
        return json.load(handle)
