from pydantic import BaseModel, Field


class GeneModel(BaseModel):
    id: str
    name: str
    description: str
    sequence: str
    baseline_expression: float
    protein_id: str
    traits: list[str] = Field(default_factory=list)
    pathway: str
    biological_effects: dict[str, float] = Field(default_factory=dict)
