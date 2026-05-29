import sys
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from network_security_mlops.constant.training_pipeline import TARGET_COLUMN
from network_security_mlops.constant.training_pipeline import (
    DATA_TRANSFORMATION_IMPUTER_PARAMS,
)

from network_security_mlops.entity.artifact_entity import (
    DataTransformationArtifact,
    DataValidationArtifact,
)

from network_security_mlops.entity.config_entity import DataTransformationConfig
from network_security_mlops.utils.exception import NetworkSecurityException
from network_security_mlops.utils.logger import logger
from network_security_mlops.utils.io_utils import save_numpy_array_data, save_object


class DataTransformation:
    def __init__(
        self,
        data_validation_artifact: DataValidationArtifact,
        data_transformation_config: DataTransformationConfig,
    ):
        try:
            # Store validation artifact
            self.data_validation_artifact = data_validation_artifact
            # Store transformation config
            self.data_transformation_config = data_transformation_config

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

    @staticmethod
    def get_data_transformer_object() -> Pipeline:
        """
        Create preprocessing pipeline
        """
        try:
            logger.info("Initializing KNNImputer")

            imputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            processor = Pipeline([("imputer", imputer)])

            return processor

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_data_transformation(self) -> DataTransformationArtifact:
        """
        Start data transformation pipeline
        """
        try:
            logger.info("Starting data transformation")

            # Read validated train/test datasets
            train_df = self.read_data(
                self.data_validation_artifact.valid_train_file_path
            )
            test_df = self.read_data(self.data_validation_artifact.valid_test_file_path)

            # Split train input and target features
            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN])
            target_feature_train_df = train_df[TARGET_COLUMN].replace(-1, 0)

            # Split test input and target features
            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN])
            target_feature_test_df = test_df[TARGET_COLUMN].replace(-1, 0)

            # Get preprocessing object
            preprocessor = self.get_data_transformer_object()

            # Fit on train data
            preprocessor_object = preprocessor.fit(input_feature_train_df)

            # Transform train data
            transformed_input_train_feature = preprocessor_object.transform(
                input_feature_train_df
            )

            # Transform test data
            transformed_input_test_feature = preprocessor_object.transform(
                input_feature_test_df
            )

            # Combine transformed features with target
            train_arr = np.c_[
                transformed_input_train_feature, np.array(target_feature_train_df)
            ]
            test_arr = np.c_[
                transformed_input_test_feature, np.array(target_feature_test_df)
            ]

            logger.info("Saving transformed numpy arrays")

            # Save transformed train array
            save_numpy_array_data(
                self.data_transformation_config.transformed_train_file_path,
                array=train_arr,
            )

            # Save transformed test array
            save_numpy_array_data(
                self.data_transformation_config.transformed_test_file_path,
                array=test_arr,
            )

            logger.info("Saving preprocessor object")

            # Save preprocessing object
            save_object(
                self.data_transformation_config.transformed_object_file_path,
                preprocessor_object,
            )

            # Save final preprocessor
            save_object(
                Path("final_model") / "preprocessor.joblib", preprocessor_object
            )

            logger.info("Data transformation completed")

            # Create transformation artifact
            data_transformation_artifact = DataTransformationArtifact(
                transformed_object_file_path=(
                    self.data_transformation_config.transformed_object_file_path
                ),
                transformed_train_file_path=(
                    self.data_transformation_config.transformed_train_file_path
                ),
                transformed_test_file_path=(
                    self.data_transformation_config.transformed_test_file_path
                ),
            )

            return data_transformation_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)
