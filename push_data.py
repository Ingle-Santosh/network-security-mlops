import os
import sys
import json
import certifi
import pymongo
import pandas as pd
from typing import List
from pathlib import Path
from dotenv import load_dotenv


from network_security_mlops.utils.exception import NetworkSecurityException
from network_security_mlops.utils.logger import logger

load_dotenv()
MONGO_DB_URL = os.getenv("MONGO_DB_URL")
ca = certifi.where()

class NetworkDataExtract:
    """
    Extract data from CSV and insert into MongoDB.
    """

    def __init__(self) -> None:
        try:
            if MONGO_DB_URL is None:
                raise Exception(
                    "MongoDB URL not found in environment variables."
                )

            self.mongo_client = pymongo.MongoClient(
                MONGO_DB_URL,
                tls=True,
                tlsCAFile=ca,
                serverSelectionTimeoutMS=5000
            )

            # Validate MongoDB connection
            self.mongo_client.admin.command("ping")

            logger.info("MongoDB connection established successfully.")

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def csv_to_json_converter(self, file_path: Path) -> List[dict]:
        """
        Convert CSV file into JSON records.

        Args:
            file_path (Path): Path to CSV file

        Returns:
            List[dict]: JSON records
        """

        try:
            logger.info(f"Reading CSV file from: {file_path}")

            # Read CSV file
            data = pd.read_csv(file_path, encoding="utf-8")

            # Validate dataset
            if data.empty:
                raise Exception("CSV file is empty.")

            # Reset index
            data.reset_index(drop=True, inplace=True)

            # Convert dataframe to JSON records
            records = json.loads(
                data.to_json(orient="records")
            )

            logger.info(
                f"Successfully converted CSV to JSON records. "
                f"Total records: {len(records)}"
            )

            return records

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def insert_data_to_mongodb(
        self,
        records: List[dict],
        database_name: str,
        collection_name: str
    ) -> int:
        """
        Insert records into MongoDB collection.

        Args:
            records (List[dict]): JSON records
            database_name (str): MongoDB database name
            collection_name (str): MongoDB collection name

        Returns:
            int: Number of inserted records
        """

        try:
            logger.info(
                f"Inserting {len(records)} records into "
                f"{database_name}.{collection_name}"
            )

            # Select database
            database = self.mongo_client[database_name]

            # Select collection
            collection = database[collection_name]

            # Insert records
            result = collection.insert_many(records)

            inserted_count = len(result.inserted_ids)

            logger.info(
                f"Successfully inserted {inserted_count} records into MongoDB."
            )

            return inserted_count

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def close_connection(self) -> None:
        """
        Close MongoDB connection.
        """

        try:
            self.mongo_client.close()

            logger.info("MongoDB connection closed.")

        except Exception as e:
            raise NetworkSecurityException(e, sys)

# if __name__ == '__main__':
#     # Initialize Path objects
#     # This works regardless of whether you use \ or /
#     BASE_DIR = Path(__file__).resolve().parent
#     DATA_FILE = BASE_DIR / "Network_Data" / "phisingData.csv"
    
#     DATABASE_NAME = "network_security"
#     COLLECTION_NAME = "phishing_data"
    
#     try:
#         extractor = NetworkDataExtract()
#         records = extractor.csv_to_json_converter(file_path=DATA_FILE)
#         records_count = extractor.insert_data_to_mongodb(records, DATABASE_NAME, COLLECTION_NAME)
#         logger.info(f"Successfully inserted {records_count} records.")
#     except Exception as e:
#         logger.error(f"Ingestion process failed: {e}")

