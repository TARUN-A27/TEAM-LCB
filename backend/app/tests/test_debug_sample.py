from fastapi.testclient import TestClient
from backend.app.main import app
client=TestClient(app)
def test_debug_sample():
    r=client.get("/debug-sample")
    assert r.status_code==200
    data=r.json()
    assert data["flooded pixels"]==5
    assert data["area_m2"]==2500.0
    assert data["dem_min"]==100.0
    assert data["rainfall_mm"]==50.0
    

