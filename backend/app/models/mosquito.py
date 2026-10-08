from pydantic import BaseModel, Field


class MosquitoState(BaseModel):
    position: list[float] = Field(default_factory=lambda: [0.0, 0.0, 0.0])
    energy: float = 100.0
    health: float = 100.0
    age: float = 0.0
    hunger: float = 0.1
    temperature: float = 25.0
    activity: float = 1.0
    flight_speed: float = 1.0
    body_size: float = 1.0
    behaviour: str = "IDLE"
