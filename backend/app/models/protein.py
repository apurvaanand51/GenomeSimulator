from pydantic import BaseModel, Field


class ProteinModel(BaseModel):
    id: str
    name: str
    gene_id: str
    function: str
    amino_acid_sequence: str
    activity: float = 1.0
    structural_properties: dict[str, float] = Field(default_factory=dict)
