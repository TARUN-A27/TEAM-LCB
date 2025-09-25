from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.endpoints import router as compute_router
app = FastAPI(
    title="TEAM_LCB flood demo API",
    version="0.1.0",
    description="PROTOTYPE API for AOI, DEM, ponding model, and interventions."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"ok": True, "message": "TEAM-LCB API is running"}


class DebugResponse(BaseModel):
    flooeded_pixels: int
    area_m2: float
    dem_min: float
    rainfall_mm: float


@app.get("/debug-sample", response_model=DebugResponse)
def debug_sample():

    return DebugResponse(
        flooeded_pixels=5,
        area_m2=5000.0,
        dem_min=100.0,
        rainfall_mm=200.0
    )


app.include_router(compute_router, prefix="/api")
