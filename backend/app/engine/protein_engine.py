from __future__ import annotations

import json
from pathlib import Path

from app.core.config import DATA_DIR


class ProteinEngine:
    def __init__(self, proteins_path: str | Path | None = None) -> None:
        path = Path(proteins_path) if proteins_path else DATA_DIR / "proteins" / "proteins.json"
        with open(path, "r", encoding="utf-8") as handle:
            self.proteins = json.load(handle)
        self.protein_map = {protein["id"]: protein for protein in self.proteins}

    def get_protein(self, protein_id: str) -> dict:
        return dict(self.protein_map.get(protein_id, {}))

    def get_all_proteins(self) -> list[dict]:
        return [dict(item) for item in self.proteins]

    def transform_protein(self, protein_id: str, change: dict) -> dict:
        protein = dict(self.protein_map.get(protein_id, {}))
        activity = float(change.get("activity", 1.0))
        protein["activity"] = max(0.2, activity)
        protein["amino_acid_sequence"] = protein.get("amino_acid_sequence", "")
        return protein
