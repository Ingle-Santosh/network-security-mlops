from network_security_mlops.entity.artifact_entity import (
    DataIngestionArtifact,
    DataValidationArtifact,
)
from network_security_mlops.entity.config_entity import DataValidationConfig
from network_security_mlops.utils.logger import logger
from network_security_mlops.utils.exception import NetworkSecurityException
from scipy.stats import ks_2samp
import pandas as pd
import sys
from pathlib import Path

from network_security_mlops.constant.training_pipeline import SCHEMA_FILE_PATH
from network_security_mlops.utils.io_utils import read_yaml_file, write_yaml_file


class DataValidation:
    def __init__(
        self,
        data_ingestion_artifact: DataIngestionArtifact,
        data_validation_config: DataValidationConfig,
    ):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config

            # Load schema configuration
            self._schema_config = read_yaml_file(Path(SCHEMA_FILE_PATH))

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    @staticmethod
    def read_data(file_path: Path) -> pd.DataFrame:
        """
        Read CSV file as dataframe
        """
        try:
            return pd.read_csv(file_path)

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def validate_number_of_columns(self, dataframe: pd.DataFrame) -> bool:
        """
        Validate total number of columns
        """
        try:
            required_columns = len(self._schema_config["columns"])
            dataframe_columns = len(dataframe.columns)

            logger.info(f"Required columns: {required_columns}")
            logger.info(f"Dataframe columns: {dataframe_columns}")

            return dataframe_columns == required_columns

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def detect_dataset_drift(
        self, base_df: pd.DataFrame, current_df: pd.DataFrame, threshold: float = 0.05
    ) -> bool:
        """
        Detect dataset drift using KS test
        """
        try:
            status = True
            report = {}

            for column in base_df.columns:
                # Remove null values before KS test
                d1 = base_df[column].dropna()
                d2 = current_df[column].dropna()

                test_result = ks_2samp(d1, d2)

                drift_found = bool(test_result.pvalue < threshold)

                if drift_found:
                    status = False

                report[column] = {
                    "p_value": float(test_result.pvalue),
                    "drift_status": drift_found,
                }

            # Get drift report path
            drift_report_file_path: Path = (
                self.data_validation_config.drift_report_file_path
            )

            # Create parent directory
            drift_report_file_path.parent.mkdir(parents=True, exist_ok=True)

            # Save drift report
            write_yaml_file(file_path=drift_report_file_path, content=report)

            logger.info(f"Drift report saved at: {drift_report_file_path}")

            return status

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_data_validation(self) -> DataValidationArtifact:
        """
        Start complete data validation pipeline
        """
        try:
            logger.info("Starting data validation")

            # Read train and test datasets
            train_dataframe = self.read_data(
                self.data_ingestion_artifact.trained_file_path
            )
            test_dataframe = self.read_data(self.data_ingestion_artifact.test_file_path)

            # Validate train columns
            train_status = self.validate_number_of_columns(train_dataframe)

            if not train_status:
                raise Exception("Train dataframe does not contain all required columns")

            # Validate test columns
            test_status = self.validate_number_of_columns(test_dataframe)

            if not test_status:
                raise Exception("Test dataframe does not contain all required columns")

            # Detect data drift
            drift_validation_status = self.detect_dataset_drift(
                base_df=train_dataframe, current_df=test_dataframe
            )

            # Create valid data directory
            self.data_validation_config.valid_train_file_path.parent.mkdir(
                parents=True, exist_ok=True
            )

            # Save validated train dataset
            train_dataframe.to_csv(
                self.data_validation_config.valid_train_file_path,
                index=False,
                header=True,
            )

            # Save validated test dataset
            test_dataframe.to_csv(
                self.data_validation_config.valid_test_file_path,
                index=False,
                header=True,
            )

            logger.info("Data validation completed")

            # Create validation artifact
            data_validation_artifact = DataValidationArtifact(
                drift_validation_status=drift_validation_status,
                valid_train_file_path=(
                    self.data_validation_config.valid_train_file_path
                ),
                valid_test_file_path=(self.data_validation_config.valid_test_file_path),
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=(
                    self.data_validation_config.drift_report_file_path
                ),
            )

            return data_validation_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)
