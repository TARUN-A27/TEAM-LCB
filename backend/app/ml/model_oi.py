import joblib
from pathlib import Path

MODELS_DIR = Path("models")

def save_model(model,name:str):
    MODELS_DIR.mkdir(exist_ok=True)
    path = MODELS_DIR / f"{name}.pkl"
    joblib.dump(model,path)
    return str(path)

def load_model(name:str):
    path = MODELS_DIR /f"{name}.pkl"
    if not path.exists():
        raise FileNotFoundError(f"model {name} not found at{path}")
    return joblib.load(path)

