import geopandas as gpd
from backend.app.services.interventions import generate_simple_interventions

def test_generate_interventions():
    poly={
        "type": "Polygon",
        "coordinates": [
            [
                [72.896,19.118],
                [72.897,19.118],
                [72.897,19.119],
                [72.896,19.119],
                [72.896,19.118]
            ]
        ]
    }

    gdf=gpd.GeoDataFrame.from_features({
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": poly,
                "properties": {}
            }
        ]
    }, crs="EPSG:4326")

    res = generate_simple_interventions(gdf)
    assert hasattr(res, "geometry")
    assert len(res) >= 1
    