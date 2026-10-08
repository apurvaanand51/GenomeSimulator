from __future__ import annotations

import json

from app.core.config import DATA_DIR


def load_genome() -> dict:
    with open(DATA_DIR / "genes" / "genes.json", "r", encoding="utf-8") as handle:
        genes = json.load(handle)
    return {"genes": genes, "reference_genome": genes}
