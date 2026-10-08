from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_and_traits_endpoints():
    health = client.get("/api/health")
    assert health.status_code == 200
    assert health.json()["status"] == "ok"

    traits = client.get("/api/traits")
    assert traits.status_code == 200
    assert len(traits.json()["traits"]) > 0


def test_genome_and_protein_endpoints():
    genome = client.get("/api/genome")
    assert genome.status_code == 200
    assert genome.json()["genes"]

    gene = client.get("/api/genome/GENE_FLIGHT")
    assert gene.status_code == 200
    assert gene.json()["id"] == "GENE_FLIGHT"

    proteins = client.get("/api/proteins")
    assert proteins.status_code == 200
    assert len(proteins.json()["proteins"]) > 0


def test_edit_and_simulate_endpoints():
    payload = {"trait_id": "flight_speed", "value": 1.2}
    mutation = client.post("/api/genome/edit", json=payload)
    assert mutation.status_code == 200
    assert mutation.json()["gene_id"] == "GENE_FLIGHT"

    simulate = client.post("/api/simulate", json={"flight_speed": 1.2, "energy": 75, "temperature": 29})
    assert simulate.status_code == 200
    assert "behaviour" in simulate.json()["state"]

    explain = client.post("/api/explain", json={"trait_id": "flight_speed", "value": 1.2})
    assert explain.status_code == 200
    assert "trait" in explain.json()
