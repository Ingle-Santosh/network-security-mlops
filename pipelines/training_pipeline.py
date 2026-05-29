from pathlib import Path
import sys

from network_security_mlops.utils.logger import logger
from network_security_mlops.utils.exception import NetworkSecurityException

from network_security_mlops.components.data_ingestion import DataIngestion
from network_security_mlops.components.data_validation import DataValidation
from network_security_mlops.components.data_transformation import DataTransformation
from network_security_mlops.components.model_trainer import ModelTrainer

from network_security_mlops.entity.config_entity import (
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
    ModelTrainerConfig,
    TrainingPipelineConfig
)

from network_security_mlops.entity.artifact_entity import (
    DataIngestionArtifact,
    DataValidationArtifact,
    DataTransformationArtifact,
    ModelTrainerArtifact
)

#from network_security_mlops.cloud.s3_syncer import S3Sync

# from network_security_mlops.constant.training_pipeline import (
#     TRAINING_BUCKET_NAME
# )


class TrainingPipeline:
    def __init__(self):
        """
        Initialize training pipeline configuration
        """
        self.training_pipeline_config = (TrainingPipelineConfig())
        # self.s3_sync = S3Sync()

    def start_data_ingestion(self) -> DataIngestionArtifact:
        """
        Start data ingestion component
        """
        try:
            logger.info("Starting data ingestion")

            data_ingestion_config = DataIngestionConfig(training_pipeline_config=self.training_pipeline_config)
            data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()

            logger.info(f"Data ingestion completed: "f"{data_ingestion_artifact}")

            return data_ingestion_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def start_data_validation(self, data_ingestion_artifact: DataIngestionArtifact) -> DataValidationArtifact:
        """
        Start data validation component
        """
        try:
            logger.info("Starting data validation")

            data_validation_config = DataValidationConfig(training_pipeline_config=self.training_pipeline_config)
            data_validation = DataValidation(data_ingestion_artifact=data_ingestion_artifact,
                                             data_validation_config=data_validation_config)
            data_validation_artifact = data_validation.initiate_data_validation()

            logger.info(f"Data validation completed: "f"{data_validation_artifact}")

            return data_validation_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def start_data_transformation(self, data_validation_artifact: DataValidationArtifact) -> DataTransformationArtifact:
        """
        Start data transformation component
        """
        try:
            logger.info("Starting data transformation")

            data_transformation_config = DataTransformationConfig(training_pipeline_config=self.training_pipeline_config)
            data_transformation = DataTransformation(data_validation_artifact=data_validation_artifact, 
                                                     data_transformation_config=data_transformation_config)

            data_transformation_artifact = data_transformation.initiate_data_transformation()

            logger.info(f"Data transformation completed: "f"{data_transformation_artifact}")

            return data_transformation_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def start_model_trainer(self,data_transformation_artifact: DataTransformationArtifact) -> ModelTrainerArtifact:
        """
        Start model training component
        """
        try:
            logger.info("Starting model trainer")

            model_trainer_config = ModelTrainerConfig(training_pipeline_config=self.training_pipeline_config)
            model_trainer = ModelTrainer(model_trainer_config=model_trainer_config,
                                         data_transformation_artifact=data_transformation_artifact)

            model_trainer_artifact = (model_trainer.initiate_model_trainer())

            logger.info(f"Model training completed: "f"{model_trainer_artifact}")

            return model_trainer_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def sync_artifact_dir_to_s3(self) -> None:
        """
        Upload artifacts directory to S3
        """
        try:
            aws_bucket_url = (
                f"s3://{TRAINING_BUCKET_NAME}"
                f"/artifact/"
                f"{self.training_pipeline_config.timestamp}"
            )

            self.s3_sync.sync_folder_to_s3(
                folder=(
                    self.training_pipeline_config.artifact_dir
                ),
                aws_bucket_url=aws_bucket_url
            )

            logger.info("Artifact directory synced to S3")

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def sync_saved_model_dir_to_s3(self) -> None:
        """
        Upload saved model directory to S3
        """
        try:
            aws_bucket_url = (
                f"s3://{TRAINING_BUCKET_NAME}"
                f"/final_model/"
                f"{self.training_pipeline_config.timestamp}"
            )

            self.s3_sync.sync_folder_to_s3(
                folder=(
                    self.training_pipeline_config.model_dir
                ),
                aws_bucket_url=aws_bucket_url
            )

            logger.info("Saved model directory synced to S3")

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def run_pipeline(self) -> ModelTrainerArtifact:
        """
        Execute complete ML pipeline
        """
        try:
            logger.info("Training pipeline started")

            # Step 1: Data ingestion
            data_ingestion_artifact = (self.start_data_ingestion())

            # Step 2: Data validation
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)

            # Step 3: Data transformation
            data_transformation_artifact = self.start_data_transformation(data_validation_artifact=data_validation_artifact)



            # Step 4: Model training
            model_trainer_artifact =  self.start_model_trainer(data_transformation_artifact = data_transformation_artifact )

            # Upload artifacts to S3
            # self.sync_artifact_dir_to_s3()

            # # Upload final model to S3
            # self.sync_saved_model_dir_to_s3()

            logger.info("Training pipeline completed successfully")

            return model_trainer_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)