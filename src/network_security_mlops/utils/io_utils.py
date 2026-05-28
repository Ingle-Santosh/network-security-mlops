import sys
import json
import yaml
import joblib
import numpy as np
from pathlib import Path
from typing import Any

from network_security_mlops.utils.logger import logger
from network_security_mlops.utils.exception import NetworkSecurityException
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score


def read_yaml_file(file_path: Path) -> dict:
    """
    Read YAML file and return content as dictionary
    """
    try:
        # Open and load YAML file
        with open(file_path, "r") as yaml_file:
            content = yaml.safe_load(yaml_file)

        return content

    except Exception as e:
        raise NetworkSecurityException(e, sys) from e
    
def write_yaml_file(file_path: Path, content: object, replace: bool = False) -> None:
    """
    Write content into YAML file
    """
    try:
        # Remove existing file if replace=True
        if replace and file_path.exists():
            file_path.unlink()

        # Create parent directories
        file_path.parent.mkdir(parents=True, exist_ok=True)

        # Write YAML content
        with open(file_path, "w") as file:
            yaml.dump(content, file)

    except Exception as e:
        logger.exception("Failed to write YAML file")
        raise NetworkSecurityException(e, sys)
    

def save_numpy_array_data(file_path: Path, array: np.ndarray) -> None:
    """
    Save numpy array to file
    """
    try:
        # Create parent directory
        file_path.parent.mkdir(parents=True, exist_ok=True)

        # Save numpy array
        with open(file_path, "wb") as file_obj:
            np.save(file_obj, array)

    except Exception as e:
        raise NetworkSecurityException(e, sys)


def save_object(file_path: Path, obj: object) -> None:
    """
    Save object using joblib
    """
    try:
        logger.info(f"Saving object at: {file_path}")

        # Create parent directory
        file_path.parent.mkdir(parents=True, exist_ok=True)

        # Save object
        joblib.dump(obj, file_path)

        logger.info("Object saved successfully")

    except Exception as e:
        raise NetworkSecurityException(e, sys)


def load_object(file_path: Path) -> object:
    """
    Load joblib object
    """
    try:
        # Check file existence
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        # Load object
        return joblib.load(file_path)

    except Exception as e:
        raise NetworkSecurityException(e, sys)
    
def load_numpy_array_data(file_path: Path) -> np.ndarray:
    """
    load numpy array data from file
    file_path: str location of file to load
    return: np.array data loaded
    """
    try:
        # Load numpy array
        with open(file_path, "rb") as file_obj:
            return np.load(file_obj)

    except Exception as e:
        raise NetworkSecurityException(e, sys)
    

def evaluate_models(X_train, y_train, X_test, y_test, models: dict, param: dict) -> dict:
    """
    Train and evaluate multiple models
    """
    try:
        report = {}

        # Iterate through all models
        for model_name, model in models.items():
            logger.info(f"Training model: {model_name}")

            # Get hyperparameters
            params = param.get(model_name, {})

            # Apply GridSearchCV if parameters exist
            if params:
                grid_search = GridSearchCV(
                    estimator=model,
                    param_grid=params,
                    cv=3,
                    n_jobs=-1,
                    verbose=1
                )
                grid_search.fit(X_train, y_train)

                # Set best parameters
                model.set_params(**grid_search.best_params_)

            # Train model
            model.fit(X_train, y_train)

            # Predictions
            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test)

            # Accuracy scores
            train_model_score = accuracy_score(y_train, y_train_pred)

            test_model_score = accuracy_score(y_test, y_test_pred)

            logger.info(
                f"{model_name} -> "
                f"Train Accuracy: {train_model_score:.4f}, "
                f"Test Accuracy: {test_model_score:.4f}"
            )

            # Store test accuracy
            report[model_name] = test_model_score

        return report

    except Exception as e:
        raise NetworkSecurityException(e, sys)