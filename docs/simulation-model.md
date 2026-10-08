# Simulation model

The mosquito simulation uses a small state machine that updates body state and movement according to the current biological values.

## Behaviours

- IDLE: default resting behaviour
- SEARCHING_FOR_FOOD: triggered by hunger and low energy
- MOVING: engaged when flight speed and activity are high
- RESTING: engaged when energy is low
- AVOIDING_HEAT: triggered by elevated temperature
- REPRODUCING: available as a state label in the conceptual model

## State update logic

Energy, behaviour, and movement are recalculated every simulation step using the most recent trait and biology values.

This is intentionally a lightweight educational model designed to illustrate causal propagation rather than biological realism.
