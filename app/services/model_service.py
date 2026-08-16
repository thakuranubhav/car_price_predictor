import joblib
import pandas as pd
from app.core.config import settings
from app.cache.redis_cache import get_cached_prediction, set_cached_prediction


def load_model():
    model_path = settings.MODEL_PATH
    if not model_path.exists():
        raise FileNotFoundError(
            f"Model file not found at '{model_path}'. Train the model or fix MODEL_PATH."
        )
    return joblib.load(model_path)


model = load_model()

def predict_car_price(data: dict):
    cache_key = " ".join([str(val) for val in data.values()])

    cached = get_cached_prediction(cache_key)

    if cached:
        return cached

    input_data = pd.DataFrame([data])
    prediction = model.predict(input_data)[0]

    result = {
        "prediction": float(prediction)
    }

    set_cached_prediction(cache_key, result)

    return result
