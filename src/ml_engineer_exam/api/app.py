import joblib
import pandas as pd
import uvicorn
from fastapi import FastAPI
from loguru import logger
from magnum import Magnum
from ml_engineer_exam.config import MLConfig
from ml_engineer_exam.model import run_model
from ml_engineer_exam.model.utils import HousingModel
from ml_engineer_exam.prediction import run_prediction
from pydantic import BaseModel

app = FastAPI(title="ML Housing Price Prediction API", version="0.1.0")

# Wrap the FastAPI app with Magnum to make it compatible with AWS Lambda since it needs a hanlder
handler = Magnum(app)


class PredictionInput(BaseModel):
    model_name: str = "linear"
    MedInc: float = 1.6812
    HouseAge: float = 25.0
    AveRooms: float = 4.192200557103064
    AveBedrms: float = 1.0222841225626742
    Population: float = 1392.0
    AveOccup: float = 3.877437325905293
    Latitude: float = 36.06
    Longitude: float = -119.01


class PredictionResponse(BaseModel):
    status: str
    model_name: str
    predicted_value: float
    input_data: dict


class TrainRequest(BaseModel):
    model_name: str = "linear"


@app.get("/ping")
def ping() -> dict:
    """Health check endpoint."""
    return {"status": "healthy", "message": "API is running"}


@app.post("/train")
def train(request: TrainRequest) -> dict:
    """Train a model (linear, ridge, or random_forest)."""
    try:
        logger.info(f"Starting training for model: {request.model_name}")

        config = MLConfig(model_name=request.model_name)
        housing_model = HousingModel(model_type=config.model_name)

        model, metrics = run_model(model=housing_model, ml_config=config)

        logger.info(f"Training complete for {request.model_name}")

        return {
            "status": "success",
            "model_name": request.model_name,
            "metrics": {"rmse": float(metrics["rmse"]), "mae": float(metrics["mae"]), "r2": float(metrics["r2"])},
            "model_path": str(config.model_path),
        }
    except Exception as e:
        logger.error(f"Training failed: {str(e)}")
        return {"status": "error", "message": str(e)}


@app.post("/predict", response_model=PredictionResponse)
def predict(input_data: PredictionInput) -> PredictionResponse:
    """Make a prediction using a trained model."""
    try:
        logger.info(f"Starting prediction with model: {input_data.model_name}")

        config = MLConfig(model_name=input_data.model_name)

        # Load the model and scaler
        model = joblib.load(config.model_path)
        scaler = joblib.load(config.model_path.with_name("scaler.joblib"))

        # Prepare input data
        data = pd.DataFrame(
            [
                {
                    "MedInc": input_data.MedInc,
                    "HouseAge": input_data.HouseAge,
                    "AveRooms": input_data.AveRooms,
                    "AveBedrms": input_data.AveBedrms,
                    "Population": input_data.Population,
                    "AveOccup": input_data.AveOccup,
                    "Latitude": input_data.Latitude,
                    "Longitude": input_data.Longitude,
                }
            ]
        )

        # Make prediction
        prediction = run_prediction(model=model, data=data, scaler=scaler)

        logger.info(f"Prediction complete: {prediction[0]}")

        return PredictionResponse(
            status="success",
            model_name=input_data.model_name,
            predicted_value=float(prediction[0]),
            input_data=input_data.model_dump(),
        )
    except Exception as e:
        logger.error(f"Prediction failed: {str(e)}")
        return {"status": "error", "message": str(e)}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
