import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

from backend.app.ml.model_io import save_model

def generate_synthetic_dataset(n=500):
    rng = np.random.default_rng(42)
    rows = []
    for i in range(n):
        area = rng.uniform(100, 1000)
        storage = rng.uniform(10, 500)
        lat = rng.uniform(18.9, 19.2)
        lon = rng.uniform(72.8, 73.0)

        reduction = storage * 2.0 + rng.normal(0, 20)

        utilization = min(storage,area *0.2) + rng.normal(0,5)

        rows.append({
            "area_m2": area,
            "storage_m3": storage,
            "centroid_lat": lat,
            "centroid_lon": lon,
            "label_reduction_m2": max(0, reduction),
            "label_storage_utilization_m3": max(0, utilization)
        })  

    df = pd.DataFrame(rows)
    return df
def train_models():
    df = generate_synthetic_dataset(800)

    X = df[["area_m2", "storage_m3", "centroid_lat", "centroid_lon"]]
    y_reduction = df["label_reduction_m2"]
    y_util = df["label_storage_utilization_m3"]

    x_train, X_test, y_train, Y-test = train_test_split(X, y_reduction, test_size=0.2, random_state=42)
    rf=RandomForestRegressor(n_estimators=50, random_state=42)
    rf.fit(x_train,y_train)
    preds = rf.predict(X_test)
    print("Reduction model MAE:", mean_absolute_error(y_test, preds),"R2:",r2_score(y_test,preds))
    save_model(rf, "reduction_model")

    x_train, X_test, y_train, y_test = train_test_split(X, y_util, test_size=0.2, random_state=42)
    lr = LinearRegression()
    lr.fit(x_train, y_train)
    preds = lr.predict(X_test)  
    print("Utilization model MAE:", mean_absolute_error(y_test, preds), "R2:", r2_score(y_test, preds))
    save_model(lr, "utilization_model")
    