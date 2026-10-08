from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from app.api.genome import load_genome
from app.api.proteins import load_proteins
from app.api.traits import load_traits
from app.api.biology import load_pathways
from app.engine.biology_engine import BiologyEngine
from app.engine.genome_engine import GenomeEngine
from app.engine.protein_engine import ProteinEngine
from app.engine.simulation_engine import SimulationEngine
from app.engine.trait_engine import TraitEngine
from app.services.experiment_service import ExperimentService

app = FastAPI(title="GenomeSim API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TraitEditRequest(BaseModel):
    trait_id: str = Field(..., description="Trait identifier, such as flight_speed")
    value: float = Field(..., ge=0.5, le=1.5)


class SimulationRequest(BaseModel):
    flight_speed: float = 1.0
    energy: float = 100.0
    temperature: float = 25.0
    hunger: float = 0.3


class ExplainRequest(BaseModel):
    trait_id: str = "flight_speed"
    value: float = 1.2


genome_engine = GenomeEngine()
trait_engine = TraitEngine()
protein_engine = ProteinEngine()
biology_engine = BiologyEngine()
experiment_service = ExperimentService()
simulation_engine = SimulationEngine()


@app.get("/health")
@app.get("/api/health")
def health() -> dict:
    return {"status": "ok", "service": "GenomeSim"}


@app.get("/api/traits")
def get_traits() -> dict:
    return {"traits": load_traits()}


@app.get("/api/genome")
def get_genome() -> dict:
    return genome_engine.get_reference_genome()


@app.get("/api/genome/{gene_id}")
def get_gene(gene_id: str) -> dict:
    try:
        return genome_engine.get_gene(gene_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.post("/api/genome/edit")
def edit_genome(request: TraitEditRequest) -> dict:
    trait = trait_engine.get_trait(request.trait_id)
    if not trait:
        raise HTTPException(status_code=404, detail=f"Trait {request.trait_id} not found")
    genes = trait_engine.get_affected_genes(request.trait_id, request.value)
    if not genes:
        raise HTTPException(status_code=400, detail="No genes affected by this trait")
    results = [genome_engine.edit_gene(gene_id, request.value) for gene_id in genes]
    return results[0] if results else {"message": "No mutation applied"}


@app.post("/api/simulate")
def simulate(request: SimulationRequest) -> dict:
    state = simulation_engine.step({
        "flight_speed": request.flight_speed,
        "energy": request.energy,
        "temperature": request.temperature,
        "hunger": request.hunger,
    })
    return {"state": state, "message": "Simulation updated"}


@app.post("/api/reset")
def reset_genome() -> dict:
    genome_engine.reset_genome()
    simulation_engine.state = {
        "position": [0.0, 0.0, 0.0],
        "energy": 100.0,
        "health": 100.0,
        "age": 0.0,
        "hunger": 0.2,
        "temperature": 25.0,
        "activity": 1.0,
        "flight_speed": 1.0,
        "body_size": 1.0,
        "behaviour": "IDLE",
    }
    return {"status": "reset"}


@app.post("/api/explain")
def explain(request: ExplainRequest) -> dict:
    return simulation_engine.create_explanation_chain(request.trait_id, request.value)


@app.get("/api/proteins")
def get_proteins() -> dict:
    return {"proteins": load_proteins()}


@app.get("/api/proteins/{protein_id}")
def get_protein(protein_id: str) -> dict:
    protein = protein_engine.get_protein(protein_id)
    if not protein:
        raise HTTPException(status_code=404, detail=f"Protein {protein_id} not found")
    return protein


@app.get("/api/biology")
def get_biology() -> dict:
    values = {"flight_speed": 1.2, "metabolism": 1.1, "body_size": 1.1, "temperature_tolerance": 1.15}
    return {"parameters": biology_engine.calculate_biological_state(values), "pathways": load_pathways()}


@app.get("/")
def root() -> dict:
    return {"message": "GenomeSim API is running"}
