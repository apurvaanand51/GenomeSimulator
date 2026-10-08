from __future__ import annotations

from app.engine.simulation_engine import SimulationEngine


def simulate_step(payload: dict) -> dict:
    engine = SimulationEngine()
    return engine.step(payload)
