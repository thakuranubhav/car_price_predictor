# Car Price Predictor API

A FastAPI-based machine learning service for predicting used car prices from structured vehicle attributes. The project includes a trained scikit-learn model, JWT-based authentication, Redis caching, and a monitoring stack powered by Prometheus and Grafana.

## Overview

This project combines three pieces:

1. A regression model trained on used-car listing data.
2. A FastAPI service that exposes login and prediction endpoints.
3. An observability layer using Prometheus metrics and Grafana dashboards, packaged with Docker Compose.

The repository already includes:

- A dataset at `app/data/car-details.csv`
- A serialized model at `app/models/model.joblib`
- Container orchestration for the API, Redis, Prometheus, and Grafana

## Features

- FastAPI REST API with automatic interactive docs
- JWT token generation through a login endpoint
- Car price prediction from structured input features
- Redis-backed response caching for repeated requests
- Prometheus instrumentation via `prometheus_fastapi_instrumentator`
- Grafana and Prometheus services for metrics visualization
- Training script for rebuilding the model artifact

## Tech Stack

- Python 3.10
- FastAPI
- Uvicorn
- scikit-learn
- pandas / NumPy
- Redis
- Prometheus
- Grafana
- Docker Compose

## Project Structure

```text
car_price_predictor/
|-- app/
|   |-- api/                  # API routes
|   |-- cache/                # Redis caching helpers
|   |-- core/                 # Settings, auth helpers, exceptions
|   |-- data/                 # Training dataset
|   |-- middleware/           # Request logging middleware
|   |-- models/               # Serialized ML model
|   |-- notebook/             # Exploration notebook
|   |-- services/             # Prediction service logic
|   `-- training/             # Model training utilities/scripts
|-- docker-compose.yml        # API + Redis + Prometheus + Grafana
|-- dockerfile                # API container image
|-- prometheus.yml            # Prometheus scrape config
|-- requirements.txt          # Python dependencies
`-- .env                      # Local environment variables
```

## Model Inputs

The `/predict` endpoint expects the following request body:

```json
{
  "company": "Maruti",
  "year": 2018,
  "owner": "First Owner",
  "fuel": "Petrol",
  "seller_type": "Dealer",
  "transmission": "Manual",
  "km_driven": 42000,
  "mileage_mpg": 18.9,
  "engine_cc": 1197,
  "max_power_bhp": 81.8,
  "torque_nm": 113.0,
  "seats": 5,
  "selling_price": 550000
}
```

Fields are passed directly into the trained model pipeline. The training script drops `name`, `model`, and `edition` from the dataset and learns from the remaining columns.

## Authentication Flow

The API exposes a simple login endpoint:

- `POST /login`

Current hard-coded credentials in the codebase:

- Username: `admin`
- Password: `admin`

On success, the endpoint returns a JWT access token. Use that token in the `token` header when calling protected endpoints.

Example login request:

```bash
curl -X POST "http://localhost:8000/login" \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"admin\",\"password\":\"admin\"}"
```

Example prediction request:

```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -H "token: <your-jwt-token>" \
  -d "{\"company\":\"Maruti\",\"year\":2018,\"owner\":\"First Owner\",\"fuel\":\"Petrol\",\"seller_type\":\"Dealer\",\"transmission\":\"Manual\",\"km_driven\":42000,\"mileage_mpg\":18.9,\"engine_cc\":1197,\"max_power_bhp\":81.8,\"torque_nm\":113.0,\"seats\":5,\"selling_price\":550000}"
```

## API Endpoints

- `GET /docs` - Swagger UI
- `GET /openapi.json` - OpenAPI schema
- `POST /login` - Generate JWT token
- `POST /predict` - Predict car price
- `GET /metrics` - Prometheus metrics endpoint

## Environment Variables

The project currently reads these values from `.env`:

```env
API_KEY=demo_key
JWT_SECRET_KEY=JWT_SECRET_KEY
REDIS_URL=redis://localhost:6379
```

Notes:

- `JWT_SECRET_KEY` is used to sign and validate tokens.
- `REDIS_URL` is used by the cache layer.
- `API_KEY` exists in configuration and dependency code, though the current prediction route relies on the `token` header and does not actively enforce an API key.

## Local Development

### 1. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Start Redis

You need a Redis instance running locally if you are not using Docker Compose.

Example using Docker:

```bash
docker run -d --name redis -p 6379:6379 redis:7-alpine
```

### 4. Run the API

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.

## Run with Docker Compose

This is the easiest way to launch the full stack.

```bash
docker compose up --build
```

Services exposed by the compose file:

- FastAPI API: `http://localhost:8000`
- Prometheus: `http://localhost:9090`
- Grafana: `http://localhost:3000`
- Redis: `localhost:6379`

Default Grafana credentials:

- Username: `admin`
- Password: `admin`

## Training the Model

To retrain the model from the bundled dataset:

```bash
python app/training/train_model.py
```

The training pipeline:

- Removes duplicate rows
- Drops `name`, `model`, and `edition`
- Splits data into train and test sets
- Applies numeric imputation and scaling
- Applies categorical imputation and one-hot encoding
- Trains a `RandomForestRegressor`
- Saves the trained artifact to the model directory

## Monitoring and Metrics

The app is instrumented with Prometheus through:

- `prometheus_fastapi_instrumentator`

Prometheus scrapes:

- Target: `web:8000`
- Metrics path: `/metrics`
- Scrape interval: `15s`

Use Grafana to connect to Prometheus and build dashboards for:

- Request counts
- Request latency
- HTTP status distribution
- Error trends

## Implementation Notes

These details are useful if you plan to extend the project:

- The trained model is loaded at application startup from `app/models/model.pkl` in configuration, while the repository currently stores a model artifact as `app/models/model.joblib`.
- The training script also writes a model under `app/training/app/models/model.joblib` based on its relative import/path behavior.
- The prediction schema currently includes `selling_price` in the request body, because that field is still part of the route model definition.
- Redis cache helper and prediction service code indicate caching is intended, though the current implementation may need refinement for production use.

If you want, this README can be followed by a cleanup pass to align the code with the documented behavior and remove these inconsistencies.

## Future Improvements

- Move credentials and secrets fully to environment variables
- Enforce proper API key or bearer-token authentication consistently
- Clean up model path inconsistencies
- Remove target leakage from the prediction request schema
- Add automated tests for auth, prediction, and cache behavior
- Add CI for linting, tests, and container checks
- Add persisted Grafana dashboards and alerts

## License

No license file is currently included in the repository. Add one if you plan to publish or distribute the project.
