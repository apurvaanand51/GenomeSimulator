from __future__ import annotations

from app.engine.biology_engine import BiologyEngine
from app.engine.genome_engine import GenomeEngine
from app.engine.protein_engine import ProteinEngine
from app.engine.simulation_engine import SimulationEngine
from app.engine.trait_engine import TraitEngine


class ExperimentService:
    def __init__(self) -> None:
        self.genome_engine = GenomeEngine()
        self.trait_engine = TraitEngine()
        self.protein_engine = ProteinEngine()
        self.biology_engine = BiologyEngine()
        self.simulation_engine = SimulationEngine()

    def apply_trait_change(self, trait_id: str, value: float) -> dict:
        genes = self.trait_engine.get_affected_genes(trait_id, value)
        gene_results = []
        for gene_id in genes:
            gene_results.append(self.genome_engine.edit_gene(gene_id, value))
        biology = self.biology_engine.calculate_biological_state({
            "flight_speed": value,
            "metabolism": value,
            "body_size": value,
            "temperature_tolerance": value,
        })
        protein = self.protein_engine.transform_protein("PROTEIN_FLIGHT", {"activity": value})
        state = self.simulation_engine.step({
            "flight_speed": value,
            "energy": 75,
            "temperature": 28,
            "hunger": 0.6,
        })
        return {
            "genes": gene_results,
            "biology": biology,
            "protein": protein,
            "state": state,
            "explanation": self.simulation_engine.create_explanation_chain(trait_id, value),
        }
