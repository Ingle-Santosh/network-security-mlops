from pathlib import Path

# from urllib.parse import urlparse
import dagshub
import os
import sys
import mlflow
from dotenv import load_dotenv
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    AdaBoostClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier,
)
from network_security_mlops.entity.artifact_entity import (
    DataTransformationArtifact,
    ModelTrainerArtifact,
)
from network_security_mlops.entity.config_entity import ModelTrainerConfig
from network_security_mlops.utils.ml_utils.model.estimator import NetworkModel
from network_security_mlops.utils.exception import NetworkSecurityException
from network_security_mlops.utils.logger import logger
from network_security_mlops.utils.io_utils import (
    save_object,
    load_object,
    load_numpy_array_data,
    evaluate_models,
)
from network_security_mlops.utils.ml_utils.metric.classification_metric import (
    get_classification_score,
)

load_dotenv()


# MLflow configuration
if os.getenv("ENABLE_MLFLOW", "false").lower() == "true":

    dagshub.init(
        repo_owner="inglesantosh09",
        repo_name="network-security-mlops",
        mlflow=True
    )
def setup_mlflow():
    mlflow_uri = os.getenv("MLFLOW_TRACKING_URI")
    mlflow_user = os.getenv("MLFLOW_TRACKING_USERNAME")
    mlflow_password = os.getenv("MLFLOW_TRACKING_PASSWORD")

    if mlflow_uri:
        os.environ["MLFLOW_TRACKING_URI"] = mlflow_uri

    if mlflow_user:
        os.environ["MLFLOW_TRACKING_USERNAME"] = mlflow_user

    if mlflow_password:
        os.environ["MLFLOW_TRACKING_PASSWORD"] = mlflow_password

setup_mlflow()


class ModelTrainer:
    def __init__(
        self,
        model_trainer_config: ModelTrainerConfig,
        data_transformation_artifact: DataTransformationArtifact,
    ):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def track_mlflow(self, best_model, classification_metric) -> None:
        """Track metrics and model using MLflow"""
        try:
            mlflow.set_registry_uri(MLFLOW_TRACKING_URI)
            # tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme

            with mlflow.start_run():
                # Log model metrics
                mlflow.log_metric("f1_score", classification_metric.f1_score)
                mlflow.log_metric(
                    "precision_score", classification_metric.precision_score
                )
                mlflow.log_metric("recall_score", classification_metric.recall_score)

                # Log model
                mlflow.sklearn.log_model(best_model, "model")
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def train_model(self, X_train, y_train, X_test, y_test) -> ModelTrainerArtifact:
        """Train and select best model"""
        try:
            logger.info("Initializing models")
            models = {
                "Random Forest": RandomForestClassifier(verbose=1),
                "Decision Tree": DecisionTreeClassifier(),
                "Gradient Boosting": GradientBoostingClassifier(verbose=1),
                "Logistic Regression": LogisticRegression(verbose=1),
                "AdaBoost": AdaBoostClassifier(),
            }

            params = {
                "Decision Tree": {"criterion": ["gini", "entropy", "log_loss"]},
                "Random Forest": {"n_estimators": [8, 16, 32, 128, 256]},
                "Gradient Boosting": {
                    "learning_rate": [0.1, 0.01, 0.05, 0.001],
                    "subsample": [0.6, 0.7, 0.75, 0.85, 0.9],
                    "n_estimators": [8, 16, 32, 64, 128, 256],
                },
                "Logistic Regression": {},
                "AdaBoost": {
                    "learning_rate": [0.1, 0.01, 0.001],
                    "n_estimators": [8, 16, 32, 64, 128, 256],
                },
            }

            logger.info("Evaluating models")
            model_report: dict = evaluate_models(
                X_train=X_train,
                y_train=y_train,
                X_test=X_test,
                y_test=y_test,
                models=models,
                param=params,
            )

            # Get best model score and name
            best_model_score = max(sorted(model_report.values()))
            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]
            best_model = models[best_model_name]
            logger.info(f"Best model found: {best_model_name}")

            # Train tracking
            y_train_pred = best_model.predict(X_train)
            classification_train_metric = get_classification_score(
                y_true=y_train, y_pred=y_train_pred
            )
            self.track_mlflow(best_model, classification_train_metric)

            # Test tracking
            y_test_pred = best_model.predict(X_test)
            classification_test_metric = get_classification_score(
                y_true=y_test, y_pred=y_test_pred
            )
            self.track_mlflow(best_model, classification_test_metric)

            logger.info("Loading preprocessing object")
            preprocessor = load_object(
                self.data_transformation_artifact.transformed_object_file_path
            )
            network_model = NetworkModel(preprocessor=preprocessor, model=best_model)

            # Save models
            self.model_trainer_config.trained_model_file_path.parent.mkdir(
                parents=True, exist_ok=True
            )
            logger.info("Saving trained model")
            save_object(
                self.model_trainer_config.trained_model_file_path, network_model
            )
            save_object(Path("final_model") / "model.joblib", best_model)
            logger.info("Model training completed")

            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                train_metric_artifact=classification_train_metric,
                test_metric_artifact=classification_test_metric,
            )
            logger.info(f"Model trainer artifact: {model_trainer_artifact}")
            return model_trainer_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        """Start model trainer pipeline"""
        try:
            logger.info("Starting model training")
            train_arr = load_numpy_array_data(
                self.data_transformation_artifact.transformed_train_file_path
            )
            test_arr = load_numpy_array_data(
                self.data_transformation_artifact.transformed_test_file_path
            )

            X_train, y_train, X_test, y_test = (
                train_arr[:, :-1],
                train_arr[:, -1],
                test_arr[:, :-1],
                test_arr[:, -1],
            )

            return self.train_model(X_train, y_train, X_test, y_test)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
