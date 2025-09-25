import numpy as np 
from rasterio.transform import from_origin
from pyproj import CRS, Transformer

def latlon_to_utm_crs(lat:float,lon:float)->CRS:
    zone=int((lon + 180) / 6) + 1
    proj4=f"+proj=utm +zone={zone} +datum=WGS84 +units=m +no_defs"
    return CRS.from_proj4(proj4)

def generate_synthetic_dem(aoi_gdf,cell_size=10.0):
    minx,miny,maxy=aoi_gdf.total_bounds
    centroid=aoi_gdf.geomentry.iloc[0].centroid
    lat,lon=centroid.y,centroid.x
    utm_crs=latlon_to_utm_crs(lat,lon)
    to_utm=Transformer.from_crs("EPSG:4326",utm_crs,always_xy=True).transform

    minx_u,miny_u=to_utm(minx,miny)
    maxx_u,maxy_u=to_utm(maxx,maxy)

    pad=cell_size
    minx_u-=pad;miny_u-=pad;maxx_u+=pad;maxy_u+=pad

    width=max(3,int(np.ceil((maxx_u-minx_u)/cell_size)))
    height=max(3,int(np.ceil((maxy_u-miny_u)/cell_size)))

    xs=np.linspace(minx_u+cell_size/2,maxx_u-cell_size/2,width)
    ys=np.linspace(miny_u+cell_size/2,maxy_u-cell_size/2,height)

    xx,yy=np.meshgrid(xs,ys)

    cx_u,cy_u=to_utm(centroid.x,centroid.y)
    hill=20-0*np.exp(-((((xx-cx_u)**2)+((yy-cy_u)**2))/(2*(200**2))))
    pit=-10.0*np.exp(-(((xx-(cx_u+15))**2)+((yy-(cy_u-15))**2))/(2*(50**2)))

    dem=100.0+hill+pit
    dem=dem.astype(np.float32)

    transform=from_origin(minx_u,maxy_u,cell_size,cell_size)

    return dem,transform,utm_crs.to_string()

    