from shapely.geometry import point,shape
from shapely.ops import transform as shp_transform
import geopandas as gpd
from pyproj import CRS, Transformer

def latlon_to_utm_crs(lat: float, lon:float) -> CRS:
    zone=int((lon+180)/6)+1
    is_nort=lat  >=0
    proj4=f"+proj=utm +zone={zone} +datum=WGS84 +units=m +no_defs"
    return CRS.from_proj4(proj4)
def create_aoi_polygon(lat:float,lon:float,radius_m:float) -> gpd.GeoDtaFrame:
    wgs84=CRS.from_epsg(4326)
    utm=latlon_to_utm_crs(lat,lon)
    to_utm=Transformer.from_crs(wgs84,utm,always_xy=True).transformer
    to_wgs = Transformer.from_crs(utm, wgs84, always_xy=True).transform
    point_wgs=point(lon,lat)
    point_utm=shp_transform(to_utm, point_wgs)
    poly_utm = point_utm.buffer(radius_m, resolution=64)
    poly_wgs = shp_transform(to_wgs, poly_utm)
    gdf = gpd.GeoDataFrame({"geometry": [poly_wgs]}, crs="EPSG:4326")
    return gdf







