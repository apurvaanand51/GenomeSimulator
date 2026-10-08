from app.engine.genome_engine import GenomeEngine
from app.engine.trait_engine import TraitEngine
from app.engine.protein_engine import ProteinEngine
from app.engine.biology_engine import BiologyEngine
from app.engine.simulation_engine import SimulationEngine


def test_genome_loading_and_mutation():
    genome = GenomeEngine()
    reference = genome.get_reference_genome()
    assert reference["genes"]
    gene = genome.get_gene("GENE_FLIGHT")
    assert gene["id"] == "GENE_FLIGHT"

    result = genome.mutate_gene("GENE_FLIGHT", 0.2)
    assert result["gene_id"] == "GENE_FLIGHT"
    assert result["mutations"]


def test_trait_modification_and_gene_expression():
    engine = TraitEngine()
    genes = engine.get_affected_genes("flight_speed", 1.2)
    assert "GENE_FLIGHT" in genes

    expression = engine.calculate_gene_expression("GENE_FLIGHT", 1.2)
    assert expression > 0


def test_protein_transformation_and_biology():
    protein_engine = ProteinEngine()
    protein = protein_engine.get_protein("PROTEIN_FLIGHT")
    assert protein["id"] == "PROTEIN_FLIGHT"

    transformed = protein_engine.transform_protein("PROTEIN_FLIGHT", {"activity": 1.2})
    assert transformed["activity"] > 0

    bio = BiologyEngine()
    params = bio.calculate_biological_state({"flight_speed": 1.2, "metabolism": 1.1, "body_size": 1.1})
    assert params["flight_speed"]["new_value"] > 0
    assert params["energy_consumption"]["new_value"] > 0


def test_simulation_and_explanation():
    sim = SimulationEngine()
    state = sim.step({"flight_speed": 1.2, "energy": 78, "temperature": 29, "hunger": 0.7})
    assert state["position"]
    assert state["behaviour"]

    explanation = sim.create_explanation_chain("flight_speed", 1.2)
    assert "trait" in explanation
    assert "gene" in explanation
