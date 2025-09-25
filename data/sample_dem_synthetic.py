from pathlib import Path
import numpy as np
import rasterio
from rasterio.transform import from_origin

def make_dem(path: Path, size: int = 10.0):

    xs = np.linspace(-250, 250, size)
    ys = np.linspace(-250, 250, size)
    xx, yy = np.meshgrid(xs, ys)

    hill = 20 * np.exp(-((xx*2 + yy2) / (2* (200*2))))
    pit = -10 * np.exp(-(((xx - 50)*2 + (yy + 50)2) / (2*(50*2))))

    dem = 100 + hill + pit
    dem =dem.astype("float32")

    transform = from_origin(-250,250,cell_size,cell_size)
    path.parent.mkdir(exist_ok=True,parents=True)

    with rasterio.open(
        path,
        "w",
        driver="GTiff",
        height=dem.shape[0],
        width=dem.shape[1],
        count=1,
        dtype="float32",
        crs="EPSG:4326",
        transform=transform,
    ) as dst:
        dst.write(dem, 1)

    print(f"Wrote {path.resolve()}")

if __name__=="_main_":
    make_dem(Path("data/sample_dem.tif"),sixe=50,cell_size=10.0)
    make_dem(Path("data/sample_dem_small.tif"),size=10,cell_size=20.0)