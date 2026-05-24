from network_security_mlops.components.data_ingestion import DataIngestion
from network_security_mlops.utils.logger import logger
from network_security_mlops.utils.exception import NetworkSecurityException
from network_security_mlops.entity.config_entity import DataIngestionConfig
from network_security_mlops.entity.config_entity import TrainingPipelineConfig

import sys


if __name__ == "__main__":
    try:
        logger.info("Starting training pipeline")

        # Create training pipeline config
        training_pipeline_config = TrainingPipelineConfig()

        # Create data ingestion config
        data_ingestion_config = DataIngestionConfig(training_pipeline_config)

        # Create data ingestion object
        data_ingestion = DataIngestion(data_ingestion_config)

        logger.info("Initiating data ingestion")

        # Start data ingestion
        data_ingestion_artifact = (data_ingestion.initiate_data_ingestion())

        logger.info("Data ingestion completed successfully")

        # Print artifact output
        print(data_ingestion_artifact)

    except Exception as e:
        logger.exception("Pipeline execution failed")
        raise NetworkSecurityException(e, sys)