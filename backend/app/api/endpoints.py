# backend/app/api/endpoints.py (corrected)
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Any, Dict
import json
import numpy as np

from shapely.geometry import shape, Point
import geopandas as gpd
from pyproj import CRS, Transformer
from rasterio.transform import from_origin

router = APIRouter()


class ComputeRequest(BaseModel):
    lat: float = Field(...,
                       description="Latitude in decimal degrees (EPSG:4326)")
    lon: float = Field(...,
                       description="Longitude in decimal degrees (EPSG:4326)")
    radius_m: float = Field(500.0, description="AOI radius in meters")
    rainfall_mm: float = Field(50.0, description="Rainfall in millimeters")


class DEMInfo(BaseModel):
    width: int
    height: int
    transform: Dict[str, Any]
    crs: str
    dem_min: float
    dem_max: float
    sample_values: list


class ComputeResponse(BaseModel):
    aoi_geojson: Dict[str, Any]
    dem_info: DEMInfo
    debug: Dict[str, Any]


def latlon_to_utm_crs(lat: float, lon: float) -> CRS:
    """
    Return an appropriate UTM CRS (metric) for a given lat/lon.
    """
    zone = int((lon + 180) / 6) + 1
    # Build a proj4 string for UTM zone (works for demo). For hemisphere-specific you'd add +south for southern lat.
    proj4 = f"+proj=utm +zone={zone} +datum=WGS84 +units=m +no_defs"
    return CRS.from_proj4(proj4)


def create_aoi_polygon(lat: float, lon: float, radius_m: float) -> gpd.GeoDataFrame:
    """
    Create AOI polygon (circle buffer) in EPSG:4326.
    Steps:
      - choose metric CRS (UTM)
      - transform lon/lat -> UTM, buffer by radius_m, transform back to WGS84
    Returns a GeoDataFrame (EPSG:4326) with one geometry.
    """
    wgs84 = CRS.from_epsg(4326)
    utm = latlon_to_utm_crs(lat, lon)

    # create transformers (callable transform functions)
    to_utm = Transformer.from_crs(wgs84, utm, always_xy=True).transform
    to_wgs = Transformer.from_crs(utm, wgs84, always_xy=True).transform

    # shapely Point expects (x=lon, y=lat)
    pt_wgs = Point(lon, lat)
    # project to utm
    pt_utm = gpd.GeoSeries([pt_wgs], crs="EPSG:4326").to_crs(
        utm.to_string()).geometry.iloc[0]
    # buffer in meters
    poly_utm = pt_utm.buffer(radius_m, resolution=64)
    # project back to wgs84
    poly_wgs = gpd.GeoSeries([poly_utm], crs=utm.to_string()).to_crs(
        "EPSG:4326").geometry.iloc[0]

    gdf = gpd.GeoDataFrame({"geometry": [poly_wgs]}, crs="EPSG:4326")
    return gdf


def generate_synthetic_dem(aoi_gdf: gpd.GeoDataFrame, cell_size=10.0):
    """
    Generate a deterministic synthetic DEM (hill + pit) covering the AOI bounding box.
    Returns: (dem_array (H,W), affine_transform, crs_string)
    """
    # AOI centroid lon/lat
    centroid = aoi_gdf.geometry.iloc[0].centroid
    lat = float(centroid.y)
    lon = float(centroid.x)

    utm_crs = latlon_to_utm_crs(lat, lon)
    to_utm = Transformer.from_crs(
        "EPSG:4326", utm_crs, always_xy=True).transform

    # AOI bounds in lon/lat
    minx, miny, maxx, maxy = aoi_gdf.total_bounds

    # convert bbox corners to UTM (x,y)
    minx_u, miny_u = to_utm(minx, miny)
    maxx_u, maxy_u = to_utm(maxx, maxy)

    # pad bounds slightly to avoid edge clipping
    pad = cell_size * 2
    minx_u -= pad
    miny_u -= pad
    maxx_u += pad
    maxy_u += pad

    width = int(np.ceil((maxx_u - minx_u) / cell_size))
    height = int(np.ceil((maxy_u - miny_u) / cell_size))

    width = max(3, width)
    height = max(3, height)

    xs = np.linspace(minx_u + cell_size / 2.0, maxx_u - cell_size / 2.0, width)
    ys = np.linspace(maxy_u - cell_size / 2.0, miny_u +
                     cell_size / 2.0, height)  # top->bottom

    xx, yy = np.meshgrid(xs, ys)

    # center of hill/pit at centroid in UTM
    cx_u, cy_u = to_utm(lon, lat)

    hill = 20.0 * np.exp(-(((xx - cx_u) ** 2) +
                         ((yy - cy_u) ** 2)) / (2 * (200.0 ** 2)))
    pit_center_x = cx_u + 0.5 * cell_size * 3
    pit_center_y = cy_u - 0.5 * cell_size * 3
    pit = -10.0 * np.exp(-(((xx - pit_center_x) ** 2) +
                         ((yy - pit_center_y) ** 2)) / (2 * (50.0 ** 2)))

    dem = 100.0 + hill + pit
    dem = dem.astype(np.float32)

    # rasterio transform: top-left origin
    transform = from_origin(minx_u, maxy_u, cell_size, cell_size)

    return dem, transform, utm_crs.to_string()


@router.post("/compute-flood-by-loc", response_model=ComputeResponse)
def compute_flood_by_loc(req: ComputeRequest):
    # Build AOI
    try:
        aoi_gdf = create_aoi_polygon(req.lat, req.lon, req.radius_m)
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"AOI creation failed: {e}")

    # Generate synthetic DEM
    try:
        dem_array, transform, dem_crs = generate_synthetic_dem(
            aoi_gdf, cell_size=10.0)
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"DEM generation failed: {e}")

    # Compute simple stats
    dem_min = float(np.nanmin(dem_array))
    dem_max = float(np.nanmax(dem_array))
    height, width = dem_array.shape

    sample_flat = dem_array.flatten()[:9].tolist()
    aoi_geojson = json.loads(aoi_gdf.to_json())

    dem_info = {
        "width": width,
        "height": height,
        "transform": {
            "origin_x": float(transform.c),
            "origin_y": float(transform.f),
            "pixel_size_x": float(transform.a),
            "pixel_size_y": float(transform.e),
        },
        "crs": dem_crs,
        "dem_min": dem_min,
        "dem_max": dem_max,
        "sample_values": sample_flat,
    }

    debug = {
        "clipped_bounds_wgs84": list(aoi_gdf.total_bounds),
        "cell_size_m": 10.0,
        "array_shape": [height, width],
    }

    return ComputeResponse(aoi_geojson=aoi_geojson, dem_info=dem_info, debug=debug)
