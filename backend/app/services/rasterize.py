import numpy as np
from rasterio.features import rasterize

def rasterize_interventions(interventions_gdf,out_shape,transform,storage_key="storage_m"):
    
    height,width = out_shape
    if interventions_gdf is None or len(interventions_gdf) ==0:
        return np.zeros((height,width), dtype=np.float32),np.ones((height,width),dtype=np.float32)

    shapes = []
    for idx,row in interventions_gdf.iterrows():
        props = row.to_dict()
        geom = row.geomentry
        area_m2 =props.get("area_m2",100.0)
        storage_m3 = props.get("storage_m3",area_m2 * 0.1)
        depth_m = storage_m3 / max(area_m2,1.0)
        shapes.append((geom,float(depth_m)))

    storage_map = rasterize(shapes, out_shape=(height,width),transform=transform,fill=0.0,dtype='float32')

    runoff_map = np.where(storage_map > 0.0,0.6,0.9).astype('float32')
    return storage_map.astype('float32'),runoff_map
    