from network_security_mlops.components.data_ingestion import DataIngestion
from network_security_mlops.components.data_validation import DataValidation
from network_security_mlops.components.data_transformation import DataTransformation
from network_security_mlops.utils.logger import logger
from network_security_mlops.utils.exception import NetworkSecurityException
from network_security_mlops.entity.config_entity import DataIngestionConfig, DataValidationConfig, DataTransformationConfig, ModelTrainerConfig
from network_security_mlops.entity.config_entity import TrainingPipelineConfig
from network_security_mlops.components.model_trainer import ModelTrainer

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

        data_validation_config = DataValidationConfig(training_pipeline_config)
        data_validation = DataValidation(data_ingestion_artifact, data_validation_config)

        logger.info("Initiating data validation")
        data_validation_artifact = data_validation.initiate_data_validation()

        logger.info("Data validation completed successfully")

        logger.info("Initiating data transformation")
        data_transformation_config = DataTransformationConfig(training_pipeline_config)
        data_transformation = DataTransformation(data_validation_artifact, data_transformation_config)
        data_transformation_artifact = data_transformation.initiate_data_transformation()

        logger.info("Data transformation completed successfully")

        logger.info("Model Training sstared")
        model_trainer_config=ModelTrainerConfig(training_pipeline_config)
        model_trainer=ModelTrainer(model_trainer_config=model_trainer_config,data_transformation_artifact=data_transformation_artifact)
        model_trainer_artifact=model_trainer.initiate_model_trainer()

        print(model_trainer_artifact)

    except Exception as e:
        logger.exception("Pipeline execution failed")
        raise NetworkSecurityException(e, sys)