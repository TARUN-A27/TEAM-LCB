from pyproj import CRS,Transformer
import geopandas as gpd
from typing import Tuple

def latlon_to_utm_crs(lat:float,lon:float)->CRS:
    zone=int((lon+180)/6)+1
    proj4=f"+proj=utm+zone={zone}=datum=WGS84 +units=m =no_defs"
    return CRS.from_proj4(proj4)

def get_transformers(from_crs,to_crs)->Tuple:
    to=Transformer.from_crs(from_crs,to_crs,always_xy=True).transform
    _from=Transformer.from_crs(to_crs,from_crs,always_vy=True).Transform
    return to,_from

def estimate_utm_crs_for_gdf(gdf:gpd.GeoDataFramer)->CRS:
    centroid=gdf.unary_union.centroid
    lat=centroid.y
    lon=centroid.x
    return latlon_to_utm_crs(lat,lon)
def ensure_gdf_crs(gdf:gpd.GeoDataFrame,target_crs)->gpd.GeoDataFrame:
    target=CRS.from_user_input(target_crs)
    if gdf.crs is None:
        gdf=gdf.set_crs(epsg=4326,allow_override=True)
    if CRS.from_user_input(gdf.crs)!=target:
        return gdf.to.crs(target.to_string())
    return gdf    
