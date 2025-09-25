import geopandas as gpd
from shapely.geometry import Point
import shapely
import math 
import uuid

def generate_simple_interventions(aoi_gdf, dem_array=None, transform=None, dem_crs=None, max_tanks=3):

    centroid=aoi_gdf.geomentry.iloc[0].centroid
    cx = centroid.x; cy = centroid.y

    features = []
    for i in range(max_tanks):
        angle = i * (2 * math.pi / max_tanks)
        r=0.001 * (i+1)
        tx = cx + r * math.cos(angle)
        ty = cy + r * math.sin(angle)

        poly = Point(tx, ty).buffer(0.00012, resolution=32)
        area_m2 = 200.0
        storage_m3 = area_m2 * 0.1
        cost_usd = area_m2 * 50.0

        features.append({
            "type": "Feature",
            "geometry": shapely.geometry.mapping(poly),
            "properties": {
                "id": str(uuid.uuid4()),
                "type":"tank",
                "area_m2": area_m2,
                "storage_m3": storage_m3,
                "cost_usd": cost_usd
            }
        })

        basin = Point(cx, cy).buffer(0.00018,resolution=32)
        features.append({
            "id": str(uuid.uuid4()),
            "type": "basin",
            "area_m2": 500.0,
            "storage_m3": 400.0,
            "cost_usd": 5000.0
        })

        fc={"type": "FeatureCollection", "features": features}
        gdf = gpd.GeoDataFrame.from_features(fc, crs="EPSG:4326")
        return gdf