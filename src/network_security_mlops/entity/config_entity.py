from pathlib import Path
from datetime import datetime
from network_security_mlops.constant import training_pipeline


class TrainingPipelineConfig:
    def __init__(self, timestamp =None):
        if timestamp is None:
            timestamp = datetime.now()
        timestamp_str = timestamp.strftime("%Y_%m_%d_%H_%M_%S")
        self.pipeline_name = training_pipeline.PIPELINE_NAME
        self.artifact_name = training_pipeline.ARTIFACT_DIR
        
        # Pathlib: Using / operator for joining paths
        self.artifact_dir: Path = Path(self.artifact_name) / timestamp_str
        self.timestamp: str = timestamp_str

class DataIngestionConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        # Base directory for ingestion
        self.data_ingestion_dir: Path = (
            training_pipeline_config.artifact_dir / 
            training_pipeline.DATA_INGESTION_DIR_NAME
        )
        
        # Feature store path
        self.feature_store_file_path: Path = (
            self.data_ingestion_dir / 
            training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR / 
            training_pipeline.FILE_NAME
        )
        
        # Ingested (Train/Test) directory
        ingested_dir = self.data_ingestion_dir / training_pipeline.DATA_INGESTION_INGESTED_DIR
        
        self.training_file_path: Path = ingested_dir / training_pipeline.TRAIN_FILE_NAME
        self.testing_file_path: Path = ingested_dir / training_pipeline.TEST_FILE_NAME
        
        # Non-path constants
        self.train_test_split_ratio: float = training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
        self.collection_name: str = training_pipeline.DATA_INGESTION_COLLECTION_NAME
        self.database_name: str = training_pipeline.DATA_INGESTION_DATABASE_NAME