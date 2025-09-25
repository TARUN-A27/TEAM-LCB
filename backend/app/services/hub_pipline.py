import geopandas as gpd
from shapely.geometry import point,LineString
import math

def detect_hub_candidates(aoi_gdf,threshold_area_m2=2000.0):
    centroid=aoi_gdf.geometry.iloc[0].centroid
    hub_poly=centroid.buffer(0.002)
    gdf=gpd.GeoDataFrame({"geometry":[hub_poly]},crs="EPSG:4326")
    gdf["score"]=1.0
    gdf["capcity_m3"]=1000.0
    return gdf
def plan_pipelines(interventions_gdf,hub_gdf):
    
    def haversine_m(a_lon,a_lat,b_lon,b_lat):
        R=6371000.0
        import math
        phi1,phi2=math.radians(a_lat),math.radians(b_lat)
        dphi=math.radians(b_lat-a_lat)
        dlambda=math.radians(b_lon-a_lon)
        a=math.sin(dphi/2.0)*2+math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2.0)*2
        c=2*math.atan2(math.sqrt(a),math.sqrt(1-a))
        return R*c
    hub_centroid=hub_gdf.geometry.iloc[0].centroid
    hx,hy=hub_centroid.x,hub_centroid.y

    lines=[]
    props=[]
    for idx,row in interventions_gdf.iterrows():
        geom=row.geometry
        c=geom.centroid
        line=LineString([(c.x,c.y),(hx,hy)])
        length_m=haversine_m(c.x,c.y,hx,hy)
        lines.append(line)
        props.append({"from_id":row.get("id",idx),"to":"hub","length_m":length_m,"pump_needed":length_m>1000})
        gdf=gpd.GeoDataFrame(props,geometry=lines,crs="EPSG:4326")
        return gdf


         
