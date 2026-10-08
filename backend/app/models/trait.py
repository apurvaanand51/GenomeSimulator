from pydantic import BaseModel


class TraitModel(BaseModel):
    id: str
    name: str
    category: str
    minimum: float
    maximum: float
    baseline: float
    unit: str
    description: str
    affected_genes: list[str]
