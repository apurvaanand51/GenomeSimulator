from __future__ import annotations

import json
from pathlib import Path

from app.core.config import DATA_DIR


class TraitEngine:
    """Deterministic mapping from trait changes to affected genes."""

    def __init__(self, traits_path: str | Path | None = None) -> None:
        path = Path(traits_path) if traits_path else DATA_DIR / "traits" / "traits.json"
        with open(path, "r", encoding="utf-8") as handle:
            self.traits = json.load(handle)
        self.trait_map = {trait["id"]: trait for trait in self.traits}

    def get_trait(self, trait_id: str) -> dict:
        return self.trait_map.get(trait_id, {})

    def get_affected_genes(self, trait_id: str, value_factor: float) -> list[str]:
        trait = self.get_trait(trait_id)
        if not trait:
            return []
        genes = trait.get("affected_genes", [])
        if value_factor == 0:
            return genes
        return genes

    def calculate_gene_expression(self, gene_id: str, trait_factor: float) -> float:
        base = {"GENE_FLIGHT": 1.0, "GENE_WING": 1.0, "GENE_METABOLISM": 1.0, "GENE_ENERGY": 1.0, "GENE_GROWTH": 1.0, "GENE_LIFESPAN": 1.0, "GENE_REPRODUCTION": 1.0, "GENE_THERMAL_RESPONSE": 1.0, "GENE_HUNGER": 1.0, "GENE_ACTIVITY": 1.0, "GENE_NAVIGATION": 1.0, "GENE_STRESS": 1.0}
        baseline = base.get(gene_id, 1.0)
        return baseline * max(0.4, trait_factor)
