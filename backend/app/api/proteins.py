from __future__ import annotations

import json

from app.core.config import DATA_DIR


def load_proteins() -> list[dict]:
    with open(DATA_DIR / "proteins" / "proteins.json", "r", encoding="utf-8") as handle:
        return json.load(handle)
