import os

TRAINING_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.dirname(TRAINING_DIR)

DATA_DIR = os.path.join(APP_DIR, "data")
DATA_FILE_NAME = "car-details.csv"
DATA_FILE_PATH = os.path.join(DATA_DIR, DATA_FILE_NAME)

MODEL_DIR_NAME = "models"
MODEL_NAME = "model.joblib"
MODEL_DIR = os.path.join(APP_DIR, MODEL_DIR_NAME)
MODEL_PATH = os.path.join(MODEL_DIR, MODEL_NAME)
