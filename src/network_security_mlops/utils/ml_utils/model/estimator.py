import sys

import pandas as pd

from network_security_mlops.utils.exception import NetworkSecurityException


class NetworkModel:
    def __init__(self, preprocessor, model):
        try:
            # Store preprocessing object
            self.preprocessor = preprocessor

            # Store trained model
            self.model = model

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def predict(self, x: pd.DataFrame):
        """
        Run prediction pipeline
        """
        try:
            # Transform input features
            x_transform = self.preprocessor.transform(x)

            # Predict output
            y_hat = self.model.predict(x_transform)

            return y_hat

        except Exception as e:
            raise NetworkSecurityException(e, sys)
