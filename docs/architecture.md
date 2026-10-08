# Architecture

## Overview

GenomeSim is organized as a two-layer product: a Python FastAPI backend and a React + TypeScript frontend. The backend owns the virtual biological engine, while the frontend focuses on interaction, visualization, and scientific explanation.

## Backend

The backend contains several focused subsystems:

- `app/api`: HTTP entry points and data loaders
- `app/engine`: genome, trait, protein, biology, and simulation logic
- `app/models`: Pydantic schemas for traits, genes, proteins, biology, and mosquitoes
- `app/services`: orchestration for experiment-level operations
- `app/core`: application configuration and path resolution

## Frontend

The frontend is a single-page laboratory dashboard built with Vite and React. It composes panels for the trait editor, genome viewer, biological effects, pathway explanation, and 3D world.

## Data flow

1. User trait change occurs in the UI.
2. Trait engine maps the trait to affected genes.
3. Genome engine creates a deterministic educational mutation.
4. Protein engine updates protein state.
5. Biology engine computes secondary effects.
6. Simulation engine adjusts mosquito behaviour.
7. UI reflects the updated causal chain and state.

## Design goals

- Keep the biological model understandable.
- Keep business logic outside the UI layer.
- Ensure the architecture can later be upgraded with real datasets.
