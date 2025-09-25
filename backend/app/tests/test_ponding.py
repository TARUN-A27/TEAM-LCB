import numpy as np
from backend.app.services.ponding import simple_ponding

def test_simple_ponding():
    dem=np.array([[100.0,101.0],[99.0,98.0]],dtype=float)
    mask,depth=simple_ponding(dem,rainfall_m=0.05)
    assert mask.shape==dem.shape
    assert depth.shape==dem.shape
    assert(depth>=0).all()
    