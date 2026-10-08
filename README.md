# GenomeSim

GenomeSim is a fictional, educational genome-to-phenotype laboratory that lets users modify virtual mosquito traits, trace the causal chain from trait to gene to phenotype, and visualize a simplified simulated biology model in a dark research-interface dashboard.

## Overview

This project demonstrates the full chain:

Trait -> Gene -> DNA -> Protein -> Biology -> Phenotype -> Behaviour -> 3D World

The system is intentionally simplified and educational. It does not claim to model real biological engineering or real mosquito genetics with scientific accuracy. Instead, it uses a consistent virtual genome and deterministic rules so the user can understand how design changes propagate through a fictional biology system.

## Features

- Trait editor with sliders and percentage change feedback
- Virtual gene and mutation tracking
- Protein visualization and activity changes
- Biological parameter dashboard
- Causal pathway explanation flow
- 3D mosquito simulation field
- FastAPI backend with scientific-model endpoints
- Data-driven design using JSON for genes, proteins, traits, and pathways

## Technology stack

- Frontend: React, TypeScript, Vite, Tailwind CSS, React Three Fiber, Recharts
- Backend: Python, FastAPI, Pydantic, NumPy, SciPy
- Data: JSON files for the virtual genome and biological models
- Testing: pytest

## Repository structure

```text
GenomeSim/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── engine/
│   │   ├── models/
│   │   ├── services/
│   │   └── main.py
│   ├── tests/
│   └── pytest.ini
├── data/
│   ├── genes/
│   ├── proteins/
│   ├── traits/
│   └── pathways/
├── docs/
├── frontend/
├── scripts/
├── .gitignore
├── README.md
└── docker-compose.yml
```

## Installation

### Backend

```bash
cd backend
python -m venv .venv
. .venv/bin/activate  # or .venv\Scripts\activate on Windows
python -m pip install -r requirements.txt
```

### Frontend

```bash
cd frontend
npm install
```

## Run the app

### Backend

```bash
cd backend
. .venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Frontend

```bash
cd frontend
npm run dev -- --host 0.0.0.0
```

Then open:

- Frontend: http://localhost:5173
- Backend: http://localhost:8000/docs

## API overview

Available endpoints include:

- GET /api/health
- GET /api/traits
- GET /api/genome
- GET /api/genome/{gene_id}
- POST /api/genome/edit
- POST /api/simulate
- POST /api/reset
- POST /api/explain
- GET /api/proteins
- GET /api/proteins/{protein_id}
- GET /api/biology

## Simulation model

The app uses a deliberately simplified deterministic model:

- A user trait change influences a mapped gene group.
- A virtual DNA mutation is generated for the affected gene.
- A protein activity modifier updates the encoded abstraction.
- Biological parameters are recomputed from simplified weighted relationships.
- Simulation behaviour is then updated to reflect travel, energy budgeting, and stress response.

## Scientific limitations

This project is not a scientific prediction engine and should not be treated as a real-world mosquito genetics model. The virtual genome, DNA sequences, and pathways are educational abstractions designed for interactive understanding.

## Future work

- Replace the virtual genome with real biological data sources and validated gene annotations
- Add richer protein structure and pathway models
- Expand the simulation to include ecology and environmental interaction
- Add experiment comparisons and more detailed saved scenarios

## Contributing

Contributions are welcome. Please keep the model clearly educational and avoid implying real-world biological certainty.

## License

This project is distributed under an open-source license to be selected by the maintainers.
