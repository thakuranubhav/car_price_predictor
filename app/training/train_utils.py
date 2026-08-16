from pathlib import Path


CURRENT_FILE_DIR = Path(__file__).resolve().parent


APP_DIR = CURRENT_FILE_DIR.parent

DATA_DIR = APP_DIR / "data"
DATA_FILE_PATH = DATA_DIR / "car-details.csv"

MODEL_DIR = APP_DIR / "models"
MODEL_NAME = "model.joblib"  # Change to "model.pkl" if your model is a .pkl file
MODEL_PATH = MODEL_DIR / MODEL_NAME