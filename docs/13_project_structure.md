# 13. Project Structure

## Overview

The **Network Security MLOps** project follows a modular and production-oriented architecture designed to support:

* End-to-End Machine Learning Pipelines
* Experiment Tracking with MLflow
* Model Serving through FastAPI
* User Interaction through Streamlit
* CI/CD Automation using GitHub Actions
* Containerized Deployment using Docker
* Reproducible Artifact Management

The repository structure separates responsibilities into independent layers, making the project easier to maintain, scale, test, and deploy.

---

# Repository Structure

```text
network-security-mlops/
│
├── api/
│   ├── app.py
│   └── routers/
│       ├── health.py
│       ├── train.py
│       └── predict.py
│
├── configs/
│   └── schema.yaml
│
├── pipelines/
│   ├── training_pipeline.py
│   └── batch_prediction.py
│
├── src/
│   └── network_security_mlops/
│
│       ├── components/
│       │   ├── data_ingestion.py
│       │   ├── data_validation.py
│       │   ├── data_transformation.py
│       │   └── model_trainer.py
│       │
│       ├── connectors/
│       │   └── s3_syncer.py
│       │
│       ├── constant/
│       │   └── training_pipeline/
│       │       └── __init__.py
│       │
│       ├── entity/
│       │   ├── config_entity.py
│       │   └── artifact_entity.py
│       │
│       └── utils/
│           ├── logger.py
│           ├── exception.py
│           ├── io_utils.py
│           │
│           └── ml_utils/
│               ├── metric/
│               │   └── classification_metric.py
│               │
│               └── model/
│                   └── estimator.py
│
├── streamlit_app/
│   └── app.py
│
├── final_model/
│   ├── model.joblib
│   └── preprocessor.joblib
│
├── Artifacts/
│
├── prediction_output/
│
├── logs/
│
├── .github/
│   └── workflows/
│       └── main.yaml
│
├── Dockerfile.api
├── Dockerfile.ui
├── docker-compose.yml
├── Makefile
├── pyproject.toml
├── requirements.txt
├── main.py
└── README.md
```

---

# Folder-Level Architecture

## 1. api/

### Purpose

Exposes the trained machine learning model as REST APIs.

### Responsibilities

* Health Monitoring
* Model Training Trigger
* Batch Prediction
* FastAPI Application Startup

### Files

| File       | Responsibility                     |
| ---------- | ---------------------------------- |
| app.py     | FastAPI application initialization |
| health.py  | Health-check endpoints             |
| train.py   | Trigger training pipeline          |
| predict.py | Generate predictions               |

---

## 2. configs/

### Purpose

Stores schema and dataset definitions.

### Files

#### schema.yaml

Contains:

* Expected dataset columns
* Feature definitions
* Data validation requirements

Example:

```yaml
columns:
  having_IP_Address: int64
  URL_Length: int64
  ...
  Result: int64
```

Used by:

* Data Validation Component
* Data Transformation Component

---

## 3. pipelines/

### Purpose

Orchestrates complete machine learning workflows.

### Files

#### training_pipeline.py

Coordinates:

```text
Data Ingestion
      ↓
Data Validation
      ↓
Data Transformation
      ↓
Model Training
```

#### batch_prediction.py

Reserved for future batch prediction workflows.

---

## 4. src/network_security_mlops/

Core business logic of the entire project.

---

# 4.1 components/

Contains individual pipeline stages.

### data_ingestion.py

Responsible for:

* MongoDB Connection
* Data Extraction
* Feature Store Creation
* Train-Test Split

Output:

```text
train.csv
test.csv
```

---

### data_validation.py

Responsible for:

* Schema Validation
* Column Validation
* Dataset Drift Detection

Output:

```text
drift_report.yaml
validated/train.csv
validated/test.csv
```

---

### data_transformation.py

Responsible for:

* Missing Value Handling
* KNN Imputation
* Feature Transformation

Output:

```text
train.npy
test.npy
preprocessing.joblib
```

---

### model_trainer.py

Responsible for:

* Model Training
* Hyperparameter Tuning
* Model Selection
* MLflow Tracking

Output:

```text
model.joblib
```

---

# 4.2 connectors/

Contains external storage connectors.

### s3_syncer.py

Future enhancement for:

* AWS S3 Integration
* Model Storage
* Artifact Backup

---

# 4.3 constant/

Centralized configuration values.

### Example

```python
TARGET_COLUMN

DATA_INGESTION_DATABASE_NAME

MODEL_TRAINER_EXPECTED_SCORE
```

Benefits:

* Single source of truth
* Easy maintenance
* Reduced hardcoding

---

# 4.4 entity/

Contains configuration and artifact definitions.

---

## config_entity.py

Creates configuration objects.

Examples:

```python
DataIngestionConfig

DataValidationConfig

DataTransformationConfig

ModelTrainerConfig
```

---

## artifact_entity.py

Defines outputs exchanged between stages.

Examples:

```python
DataIngestionArtifact

DataValidationArtifact

DataTransformationArtifact

ModelTrainerArtifact
```

These artifacts enable loose coupling between pipeline components.

---

# 4.5 utils/

Shared utility functions.

---

## logger.py

Provides centralized logging.

Features:

* File Logging
* Console Logging
* Timestamped Logs

---

## exception.py

Provides custom exception handling.

Captures:

* File Name
* Line Number
* Error Message

---

## io_utils.py

Provides helper functions for:

* YAML Operations
* Model Persistence
* Numpy Storage
* Object Serialization
* Model Evaluation

---

# 4.6 ml_utils/

Machine Learning helper utilities.

---

## metric/

### classification_metric.py

Computes:

* Precision
* Recall
* F1 Score

Returns:

```python
ClassificationMetricArtifact
```

---

## model/

### estimator.py

Defines:

```python
NetworkModel
```

Combines:

```text
Preprocessor
      +
Trained Model
```

Used during prediction.

---

# 5. streamlit_app/

### Purpose

Provides a user-friendly interface.

### Features

#### Training Trigger

```text
Run Training Pipeline
```

Calls:

```http
GET /train
```

---

#### Prediction Interface

Allows users to:

* Upload CSV Files
* Generate Predictions
* Download Results

Calls:

```http
POST /predict
```

---

# 6. final_model/

Stores production-ready artifacts.

Contents:

```text
model.joblib

preprocessor.joblib
```

Loaded during FastAPI startup.

---

# 7. Artifacts/

Stores timestamped outputs from each pipeline run.

Example:

```text
Artifacts/

└── 2026_06_11_14_30_45/

    ├── data_ingestion/

    ├── data_validation/

    ├── data_transformation/

    └── model_trainer/
```

Benefits:

* Experiment Traceability
* Reproducibility
* Auditing

---

# 8. prediction_output/

Stores prediction results generated by API requests.

Example:

```text
prediction_output/

output_ab12cd34.csv
```

---

# 9. logs/

Stores runtime logs.

Example:

```text
logs/

06_11_2026_14_25_01.log
```

Used for:

* Debugging
* Monitoring
* Troubleshooting

---

# 10. .github/workflows/

Contains CI/CD automation.

### main.yaml

Pipeline Stages:

```text
Code Push
     ↓
Linting
     ↓
Testing
     ↓
Docker Build
     ↓
Render Deployment
     ↓
Health Check
```

---

# 11. Docker Files

## Dockerfile.api

Creates FastAPI container.

Contains:

* API Layer
* Trained Models
* Prediction Service

---

## Dockerfile.ui

Creates Streamlit container.

Contains:

* Frontend Interface
* User Dashboard

---

## docker-compose.yml

Runs complete system.

Services:

```text
FastAPI
     +
Streamlit
```

Provides:

* Networking
* Health Checks
* Volume Mounting

---

# 12. Build & Dependency Management

## Makefile

Provides shortcuts.

```bash
make train

make api

make ui

make full
```

---

## pyproject.toml

Project metadata and dependencies.

Examples:

```text
FastAPI

Streamlit

Scikit-Learn

MLflow

DagsHub

MongoDB
```

---

# End-to-End Repository Flow

```text
MongoDB
    │
    ▼
Data Ingestion
    │
    ▼
Data Validation
    │
    ▼
Data Transformation
    │
    ▼
Model Training
    │
    ▼
MLflow Tracking
    │
    ▼
Model Storage
    │
    ▼
FastAPI
    │
    ▼
Streamlit UI
    │
    ▼
End User
```

---

# Key Design Principles

* Modular Architecture
* Configuration Driven Development
* Artifact-Based Communication
* Reproducible Training Runs
* Experiment Tracking
* Containerized Deployment
* Automated CI/CD
* Production-Oriented MLOps Design

This structure enables the project to scale from a local machine learning experiment into a deployable and maintainable production MLOps system.
