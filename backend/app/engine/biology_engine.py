from __future__ import annotations


class BiologyEngine:
    def calculate_biological_state(self, trait_values: dict) -> dict:
        flight_speed = float(trait_values.get("flight_speed", 1.0))
        metabolism = float(trait_values.get("metabolism", 1.0))
        body_size = float(trait_values.get("body_size", 1.0))

        flight_value = 1.0 * flight_speed * 1.2
        energy_consumption = 1.0 * flight_speed * metabolism
        energy = max(0.0, 100.0 / (1.0 + (flight_speed - 1.0) * 0.8))
        lifespan = 1.0 * (1.0 + (body_size - 1.0) * 0.2)
        temp = 1.0 * float(trait_values.get("temperature_tolerance", 1.0))

        return {
            "flight_speed": {
                "baseline_value": 1.0,
                "new_value": flight_value,
                "percent_change": round(((flight_value / 1.0) - 1.0) * 100, 2),
                "explanation": "Flight speed is increased by the trait-to-gene expression and muscle-efficiency chain.",
                "contributing_genes": ["GENE_FLIGHT", "GENE_ACTIVITY"],
            },
            "energy_consumption": {
                "baseline_value": 20.0,
                "new_value": round(20.0 * energy_consumption, 2),
                "percent_change": round(((20.0 * energy_consumption) / 20.0 - 1.0) * 100, 2),
                "explanation": "Higher flight speed causes more energetic demand under the virtual model.",
                "contributing_genes": ["GENE_FLIGHT", "GENE_METABOLISM"],
            },
            "energy": {
                "baseline_value": 100.0,
                "new_value": round(energy, 2),
                "percent_change": round(((energy / 100.0) - 1.0) * 100, 2),
                "explanation": "Available energy is moderated by the efficiency of the virtual energy conversion pathway.",
                "contributing_genes": ["GENE_ENERGY", "GENE_METABOLISM"],
            },
            "lifespan": {
                "baseline_value": 1.0,
                "new_value": round(lifespan, 2),
                "percent_change": round(((lifespan / 1.0) - 1.0) * 100, 2),
                "explanation": "Body size and maintenance investment shift the lifespan estimate in the virtual model.",
                "contributing_genes": ["GENE_LIFESPAN", "GENE_GROWTH"],
            },
            "temperature_tolerance": {
                "baseline_value": 1.0,
                "new_value": round(temp, 2),
                "percent_change": round(((temp / 1.0) - 1.0) * 100, 2),
                "explanation": "Thermal response genes adjust operability under hotter conditions.",
                "contributing_genes": ["GENE_THERMAL_RESPONSE", "GENE_STRESS"],
            },
            "body_mass": {
                "baseline_value": 1.0,
                "new_value": round(body_size, 2),
                "percent_change": round(((body_size / 1.0) - 1.0) * 100, 2),
                "explanation": "Growth gene expression modifies body-scale variables in the virtual simulation.",
                "contributing_genes": ["GENE_GROWTH"],
            },
        }
