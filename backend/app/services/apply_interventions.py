import numpy as np
def apply_storage_to_dem(dem_array, storage_map, max_subtract=5.0):
    delta = np.minimum(storage_map, max_subtract)
    new_dem = dem_array - delta
    return new_dem

def adjust_rainfall_by_runoff(rainfall_map, runoff_map):
    coeff = float(np.nanmean(runoff_map))
    return rainfall_m * coeff 

    