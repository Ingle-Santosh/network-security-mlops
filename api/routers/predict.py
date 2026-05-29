import sys
import uuid
from pathlib import Path

import pandas as pd
from fastapi import APIRouter, File, Request, UploadFile
from fastapi.responses import JSONResponse

from network_security_mlops.utils.exception import NetworkSecurityException
from network_security_mlops.utils.logger import logger

router = APIRouter(tags=["prediction"])

OUTPUT_DIR = Path("prediction_output")


@router.post("/predict")
async def predict_route(request: Request, file: UploadFile = File(...)):
    try:
        logger.info("Reading uploaded file")
        dataframe = pd.read_csv(file.file)

        # ── use model loaded at startup (no per-request disk I/O) ─────
        network_model = request.app.state.model
        logger.info("Running predictions")
        dataframe["predicted_column"] = network_model.predict(dataframe)

        # ── unique filename per request (fixes shared output.csv race) ─
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        output_path = OUTPUT_DIR / f"output_{uuid.uuid4().hex[:8]}.csv"
        dataframe.to_csv(output_path, index=False)
        logger.info("Prediction saved to %s", output_path)

        # ── return JSON instead of Jinja2 template ────────────────────
        return JSONResponse(content={
            "status": "success",
            "total_records": len(dataframe),
            "output_file": str(output_path),
            "predictions": dataframe["predicted_column"].tolist(),
            "data": dataframe.to_dict(orient="records"),
        })

    except Exception as e:
        raise NetworkSecurityException(e, sys)