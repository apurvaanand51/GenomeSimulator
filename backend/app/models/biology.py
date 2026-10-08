from pydantic import BaseModel, Field


class BiologicalState(BaseModel):
    body_mass: float = 1.0
    wing_area: float = 1.0
    flight_speed: float = 1.0
    energy: float = 100.0
    energy_consumption: float = 20.0
    metabolism_rate: float = 1.0
    lifespan: float = 1.0
    age: float = 0.0
    reproduction_rate: float = 1.0
    temperature_tolerance: float = 1.0
    activity: float = 1.0
    stress: float = 0.3
    hunger: float = 0.2
    navigation_efficiency: float = 1.0
    health: float = 100.0


class BiologicalParameter(BaseModel):
    name: str
    baseline_value: float
    new_value: float
    percent_change: float
    explanation: str
    contributing_genes: list[str] = Field(default_factory=list)
