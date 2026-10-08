from __future__ import annotations


class SimulationEngine:
    def __init__(self) -> None:
        self.time = 0.0
        self.state = {
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

    def step(self, values: dict) -> dict:
        flight_speed = float(values.get("flight_speed", 1.0))
        energy = float(values.get("energy", self.state["energy"]))
        temperature = float(values.get("temperature", self.state["temperature"]))
        hunger = float(values.get("hunger", self.state["hunger"]))

        if energy < 30:
            behaviour = "RESTING"
        elif hunger > 0.7:
            behaviour = "SEARCHING_FOR_FOOD"
        elif temperature > 32:
            behaviour = "AVOIDING_HEAT"
        elif flight_speed > 1.15:
            behaviour = "MOVING"
        else:
            behaviour = "IDLE"

        x = self.state["position"][0] + flight_speed * 0.5
        y = self.state["position"][1] + (1.0 if behaviour == "MOVING" else 0.0)
        z = self.state["position"][2] + (temperature - 25.0) * 0.05

        self.state.update({
            "position": [round(x, 2), round(y, 2), round(z, 2)],
            "energy": max(0.0, energy - (flight_speed * 0.6)),
            "activity": flight_speed,
            "flight_speed": flight_speed,
            "temperature": temperature,
            "hunger": hunger,
            "behaviour": behaviour,
        })
        self.time += 0.1
        return dict(self.state)

    def create_explanation_chain(self, trait_id: str, value: float) -> dict:
        return {
            "trait": {
                "id": trait_id,
                "label": "Trait",
                "description": f"{trait_id} increased by {value * 100:.0f}% in the educational model.",
            },
            "gene": {
                "id": "GENE_FLIGHT",
                "description": "GENE_FLIGHT expression increased under the simulated gene-expression rule.",
            },
            "dna": {
                "mutation_count": 1,
                "description": "A simulated educational mutation was introduced in the virtual genomic sequence.",
            },
            "protein": {
                "id": "PROTEIN_FLIGHT",
                "description": "The encoded protein activity increased and altered the flight apparatus.",
            },
            "pathway": {
                "id": "muscle_efficiency_pathway",
                "description": "Energy metabolism demand increased in the virtual flight pathway.",
            },
            "biology": {
                "parameter": "flight_speed",
                "description": "Energy consumption increased while available energy was reduced, changing speed behaviour.",
            },
            "phenotype": {
                "summary": "Predicted flight speed increased.",
            },
            "behaviour": {
                "state": "MOVING",
                "description": "The mosquito travels faster but consumes more energy over time.",
            },
        }
