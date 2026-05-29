import sys

from fastapi import APIRouter
from fastapi.responses import Response

from network_security_mlops.utils.exception import NetworkSecurityException
from network_security_mlops.utils.logger import logger
from pipelines.training_pipeline import TrainingPipeline

router = APIRouter(tags=["training"])


@router.get("/train")
async def train_route():
    try:
        logger.info("Starting training pipeline")
        TrainingPipeline().run_pipeline()
        logger.info("Training pipeline completed")
        return Response(content="Training completed successfully")
    except Exception as e:
        raise NetworkSecurityException(e, sys)