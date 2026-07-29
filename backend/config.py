from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "models" / "ridewise_model.joblib"
MODEL_PATH2 = BASE_DIR / "models" / "future_ridewise_model.joblib"

FEATURE_PATH = BASE_DIR / "models" / "features.joblib"
FEATURE_PATH2 = BASE_DIR / "models" / "future_features.joblib"

DATA_PATH = BASE_DIR / "data" / "processed" / "hour_features.csv"
DATA_PATH2 = BASE_DIR / "data" / "processed" / "hour_features_2.csv"