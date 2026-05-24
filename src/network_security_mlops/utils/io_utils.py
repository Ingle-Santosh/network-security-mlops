import sys
import json
import yaml
import joblib
from pathlib import Path
from typing import Any

from network_security_mlops.utils.logger import logger
from network_security_mlops.utils.exception import NetworkSecurityException


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