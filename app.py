"""student-ml-api — a minimal prediction service.

The prediction logic is deliberately trivial (input * 2). The purpose of this
service is to act as a versioned, containerised artifact for the MLOps
workflow, not to perform real inference so its kept simple. 
"""

from pathlib import Path

from fastapi import FastAPI
from pydantic import BaseModel, Field

APPLICATION_NAME = "student-ml-api"

# The VERSION file is the single source of truth for the application version,
# so a release only ever needs the version bumped in one place.
APPLICATION_VERSION = (Path(__file__).parent / "VERSION").read_text().strip()

MODEL_NAME = "double-value-model"
MODEL_VERSION = "model-1"
MODEL_DESCRIPTION = "Returns input multiplied by 2"

app = FastAPI(
    title=APPLICATION_NAME,
    version=APPLICATION_VERSION,
    description="Simple prediction API used to demonstrate a professional MLOps workflow.",
)


class PredictionRequest(BaseModel):
    

    value: float = Field(..., description="Numeric input to run the prediction on")


@app.get("/")
def root():
    return {
        "message": "Welcome to Student ML API",
        "version": APPLICATION_VERSION,
    }


@app.get("/health")
def health():
    """Health status, reporting the application and model versions separately.

    The application version and the model version change independently, so
    they are reported as distinct fields rather than a single "version".
    """
    return {
        "status": "healthy",
        "application": APPLICATION_NAME,
        "application_version": APPLICATION_VERSION,
        "model_version": MODEL_VERSION,
    }


@app.get("/model-info")
def model_info():
    return {
        "model_name": MODEL_NAME,
        "model_version": MODEL_VERSION,
        "description": MODEL_DESCRIPTION,
    }


@app.get("/version")
def version():
    return {
        "application_version": APPLICATION_VERSION,
        "model_version": MODEL_VERSION,
    }


@app.post("/predict")
def predict(request: PredictionRequest):
    return {
        "input": request.value,
        "prediction": request.value * 2,
    }


if __name__ == "__main__":
    import uvicorn

    # 0.0.0.0 so the app is reachable from outside the container.
    uvicorn.run(app, host="0.0.0.0", port=5000)
