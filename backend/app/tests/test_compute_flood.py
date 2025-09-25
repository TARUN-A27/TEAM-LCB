from fastapi.testclient import TestClient
from backednd.app.main import app

client=TestClient(app)

def test_compute_flood_by_loc():
    payload = {"lat":19.1190,"lon":72.8970,"radius":300,"rainfall_mm":100}
    r=client.post("/api/compute-flood-byloc",json=payload)
    assert r.status_code==200
    j=r.json()
    assert"aoi_geojson"in j
    assert"dem_info"in j
    assert "width" in j["dem_info"]
    assert "height" in j["dem_info"]
    assert j["dem_info"]["dem_min"] <= j["dem_info"]["dem_max"]
    