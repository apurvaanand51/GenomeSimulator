from __future__ import annotations

import json
from pathlib import Path

from app.core.config import DATA_DIR


class GenomeEngine:
    """Educational virtual genome engine. These mutations are not real-world genetic engineering instructions."""

    BASE_PAIRS = {"A": "G", "T": "A", "C": "G", "G": "C"}

    def __init__(self, genes_path: str | Path | None = None) -> None:
        path = Path(genes_path) if genes_path else DATA_DIR / "genes" / "genes.json"
        with open(path, "r", encoding="utf-8") as handle:
            self.reference_genome = json.load(handle)
        self.edited_genome = [dict(gene) for gene in self.reference_genome]

    def get_reference_genome(self) -> dict:
        return {"genes": [dict(gene) for gene in self.reference_genome]}

    def get_gene(self, gene_id: str) -> dict:
        for gene in self.edited_genome:
            if gene["id"] == gene_id:
                return dict(gene)
        raise KeyError(f"Gene {gene_id} not found")

    def reset_genome(self) -> dict:
        self.edited_genome = [dict(gene) for gene in self.reference_genome]
        return self.get_reference_genome()

    def compare_reference_vs_edited(self, gene_id: str) -> dict:
        reference = next((g for g in self.reference_genome if g["id"] == gene_id), None)
        edited = next((g for g in self.edited_genome if g["id"] == gene_id), None)
        if reference is None or edited is None:
            raise KeyError(f"Gene {gene_id} not found")
        return {
            "gene_id": gene_id,
            "reference_sequence": reference["sequence"],
            "edited_sequence": edited["sequence"],
            "mutations": self._compute_mutations(reference["sequence"], edited["sequence"]),
        }

    def edit_gene(self, gene_id: str, trait_factor: float) -> dict:
        gene = self.get_gene(gene_id)
        mutated_sequence = self._mutate_sequence(gene["sequence"], trait_factor, gene_id)
        for idx, item in enumerate(self.edited_genome):
            if item["id"] == gene_id:
                item["sequence"] = mutated_sequence
                item["baseline_expression"] = max(0.5, min(1.8, item["baseline_expression"] * (1 + trait_factor * 0.4)))
                break
        return self.compare_reference_vs_edited(gene_id)

    def mutate_gene(self, gene_id: str, trait_factor: float) -> dict:
        return self.edit_gene(gene_id, trait_factor)

    def calculating_mutation_positions(self, gene_id: str) -> list[int]:
        reference = next((g for g in self.reference_genome if g["id"] == gene_id), None)
        edited = next((g for g in self.edited_genome if g["id"] == gene_id), None)
        if reference is None or edited is None:
            return []
        return [idx for idx, (ref, edt) in enumerate(zip(reference["sequence"], edited["sequence"])) if ref != edt]

    def generate_diff(self, gene_id: str) -> dict:
        reference = next((g for g in self.reference_genome if g["id"] == gene_id), None)
        edited = next((g for g in self.edited_genome if g["id"] == gene_id), None)
        if reference is None or edited is None:
            raise KeyError(f"Gene {gene_id} not found")
        mutations = self._compute_mutations(reference["sequence"], edited["sequence"])
        return {"gene_id": gene_id, "mutation_count": len(mutations), "mutations": mutations}

    def _mutate_sequence(self, sequence: str, trait_factor: float, gene_id: str) -> str:
        factor = max(0.05, abs(trait_factor))
        index = abs(hash(gene_id)) % len(sequence)
        nucleotide = sequence[index]
        mutated = self.BASE_PAIRS.get(nucleotide, "A")
        if factor > 1.0 and index % 2 == 0:
            mutated = "C"
        chars = list(sequence)
        chars[index] = mutated
        return "".join(chars)

    def _compute_mutations(self, reference: str, edited: str) -> list[dict]:
        mutations = []
        for idx, (ref, new) in enumerate(zip(reference, edited)):
            if ref != new:
                mutations.append({"position": idx + 1, "reference": ref, "edited": new})
        return mutations
