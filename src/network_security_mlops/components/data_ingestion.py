import os
import sys
import pymongo
import numpy as np
import pandas as pd
from pathlib import Path
from typing import List
from dotenv import load_dotenv
load_dotenv()
from sklearn.model_selection import train_test_split

from network_security_mlops.utils.logger import logger
from network_security_mlops.utils.exception import NetworkSecurityException
from network_security_mlops.entity.config_entity import DataIngestionConfig
from network_security_mlops.entity.artifact_entity import DataIngestionArtifact


MONGO_DB_URL=os.getenv("MONGO_DB_URL")


class DataIngestion:
    """
    Handles:
    1. Reading data from MongoDB
    2. Saving raw data into feature store
    3. Train-test split
    4. Returning ingestion artifact
    """

    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config=data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
        
    def export_collection_as_dataframe(self)-> pd.DataFrame:
        """
        Read MongoDB collection and convert to DataFrame
        """
        try:
            logger.info("Starting MongoDB data export")
             # Read DB details from config
            database_name=self.data_ingestion_config.database_name
            collection_name=self.data_ingestion_config.collection_name

            # Create MongoDB client
            self.mongo_client=pymongo.MongoClient(MONGO_DB_URL)

            # Access collection
            collection=self.mongo_client[database_name][collection_name]

            # Convert collection data into dataframe
            df=pd.DataFrame(list(collection.find()))

            logger.info(f"Fetched {len(df)} records from MongoDB")

            # Remove MongoDB generated ID column
            if "_id" in df.columns.to_list():
                df=df.drop(columns=["_id"])
            
            # Replace invalid missing values with np.nan
            df.replace(
                ["na", "NA", "null", "Null", "None"],
                np.nan,
                inplace=True
            )

            logger.info("MongoDB export completed")

            # Close DB connection
            self.mongo_client.close()

            return df
        
        except Exception as e:
            raise NetworkSecurityException
        
        
    def export_data_into_feature_store(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        """
        Save raw dataframe into feature store
        """
        try:
            logger.info("Exporting data into feature store")

             # Get feature store path
            feature_store_file_path=self.data_ingestion_config.feature_store_file_path

            ## Create parent directories
            feature_store_file_path.parent.mkdir(parents=True,exist_ok=True)

            # Save dataframe
            dataframe.to_csv(feature_store_file_path, index=False, header=True)

            logger.info(f"Feature store file saved at: {feature_store_file_path}")

            return dataframe
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
        
    def split_data_as_train_test(self,dataframe: pd.DataFrame)->None:
        """
        Split dataframe into train and test dataset
        """
        try:
            logger.info("Performing train-test split")

            train_set, test_set = train_test_split(dataframe, test_size=self.data_ingestion_config.train_test_split_ratio, random_state=42)
            
            logger.info("Train-test split completed")

            # Get output directory
            train_file_path: Path = (self.data_ingestion_config.training_file_path)

            test_file_path: Path = (self.data_ingestion_config.testing_file_path)

            # Create parent directories
            train_file_path.parent.mkdir(parents=True, exist_ok=True)

            # Save train dataset
            train_set.to_csv(train_file_path, index=False, header=True)

            # Save test dataset
            test_set.to_csv(test_file_path, index=False, header=True)

            logger.info(f"Train file saved at: {train_file_path}")
            logger.info(f"Test file saved at: {test_file_path}")

        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def initiate_data_ingestion(self):
        """
        Execute complete data ingestion pipeline
        """
        try:
            logger.info("Starting data ingestion pipeline")

            # Read data from MongoDB using custom function
            dataframe=self.export_collection_as_dataframe()


            # Save raw data into feature store using custom function
            dataframe=self.export_data_into_feature_store(dataframe)

            # Split data into train and test using custom function
            self.split_data_as_train_test(dataframe)

            # Create ingestion artifact
            data_ingestion_artifact = DataIngestionArtifact(trained_file_path = self.data_ingestion_config.training_file_path,
                                                        test_file_path = self.data_ingestion_config.testing_file_path)
            logger.info("Data ingestion pipeline completed")

            return data_ingestion_artifact

        except Exception as e:
            raise NetworkSecurityException