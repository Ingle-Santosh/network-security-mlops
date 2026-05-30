# Network Security MLOps

# Network Security MLOps

[![CI/CD Pipeline](https://github.com/Ingle-Santosh/network-security-mlops/actions/workflows/main.yaml/badge.svg)](https://github.com/Ingle-Santosh/network-security-mlops/actions/workflows/main.yaml)

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-API-green)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-red)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue)
![MLflow](https://img.shields.io/badge/MLflow-Experiment%20Tracking-lightblue)
![DagsHub](https://img.shields.io/badge/DagsHub-MLOps-orange)
![Render](https://img.shields.io/badge/Render-Deployed-purple)

End-to-end MLOps project for Network Security Threat Detection using Machine Learning, FastAPI, Streamlit, Docker, GitHub Actions, DagsHub MLflow Tracking, MongoDB, and Render deployment.
---

## Project Overview

This project demonstrates how to take a Machine Learning model from experimentation to production using MLOps best practices.

The system trains a network security classification model, tracks experiments with MLflow, serves predictions through FastAPI, provides a Streamlit UI for batch predictions, containerizes services with Docker, and automates deployment using GitHub Actions and Render.

---

## Architecture

```text
                    ┌────────────────────┐
                    │     MongoDB        │
                    │  Source Dataset    │
                    └─────────┬──────────┘
                              │
                              ▼
                    ┌────────────────────┐
                    │ Data Ingestion     │
                    └─────────┬──────────┘
                              │
                              ▼
                    ┌────────────────────┐
                    │ Data Validation    │
                    └─────────┬──────────┘
                              │
                              ▼
                    ┌────────────────────┐
                    │ Data Transformation│
                    └─────────┬──────────┘
                              │
                              ▼
                    ┌────────────────────┐
                    │ Model Training     │
                    └─────────┬──────────┘
                              │
                              ▼
                 ┌──────────────────────────┐
                 │ MLflow + DagsHub Tracking│
                 └───────────┬──────────────┘
                             │
                             ▼
                    ┌────────────────────┐
                    │ Trained Model      │
                    │ model.joblib       │
                    │ preprocessor.joblib│
                    └─────────┬──────────┘
                              │
           ┌──────────────────┴──────────────────┐
           │                                     │
           ▼                                     ▼
 ┌─────────────────────┐             ┌─────────────────────┐
 │ FastAPI Prediction  │             │ Streamlit UI        │
 │ Service             │             │ Batch Upload UI     │
 └──────────┬──────────┘             └──────────┬──────────┘
            │                                   │
            └──────────────┬────────────────────┘
                           ▼
                  Docker Containers
                           │
                           ▼
                        Render
```

---

## Tech Stack

### Machine Learning

* Python
* Scikit-learn
* Pandas
* NumPy

### MLOps

* MLflow
* DagsHub
* GitHub Actions
* Docker
* Docker Compose

### Backend

* FastAPI
* Uvicorn

### Frontend

* Streamlit

### Database

* MongoDB Atlas

### Deployment

* Render

---

## Features

### Data Pipeline

* MongoDB data ingestion
* Schema validation
* Data transformation pipeline
* Train/Test split generation

### Model Training

* Automated training pipeline
* Experiment tracking using MLflow
* DagsHub integration
* Artifact generation

### Prediction Service

* FastAPI REST API
* Batch CSV prediction
* Health check endpoint
* OpenAPI documentation

### User Interface

* Streamlit dashboard
* CSV upload
* Prediction download
* API integration

### MLOps

* Dockerized services
* Docker Compose orchestration
* CI/CD with GitHub Actions
* Automated Render deployment
* Health monitoring

---

## Repository Structure

```text
network-security-mlops
│
├── api/
│   ├── app.py
│   └── routers/
│       ├── health.py
│       ├── predict.py
│       └── train.py
│
├── configs/
│   └── schema.yaml
│
├── final_model/
│   ├── model.joblib
│   └── preprocessor.joblib
│
├── pipelines/
│   └── training_pipeline.py
│
├── src/
│   └── network_security_mlops/
│       ├── components/
│       │   ├── data_ingestion.py
│       │   ├── data_validation.py
│       │   ├── data_transformation.py
│       │   └── model_trainer.py
│       │
│       ├── entity/
│       ├── constant/
│       ├── utils/
│       └── cloud/
│
├── streamlit_app/
│   └── app.py
│
├── .github/
│   └── workflows/
│       └── main.yaml
│
├── Dockerfile.api
├── Dockerfile.ui
├── docker-compose.yml
├── requirements.txt
├── render.yaml
└── README.md
```

---

## Local Setup

### Clone Repository

```bash
git clone https://github.com/Ingle-Santosh/network-security-mlops.git

cd network-security-mlops
```

### Create Virtual Environment

```bash
python -m venv venv
```

Activate:

Windows

```bash
venv\Scripts\activate
```

Linux/Mac

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file.

```env
MONGODB_URL_KEY=YOUR_MONGODB_CONNECTION

MLFLOW_TRACKING_URI=https://dagshub.com/<username>/<repo>.mlflow

MLFLOW_TRACKING_USERNAME=YOUR_DAGSHUB_USERNAME

MLFLOW_TRACKING_PASSWORD=YOUR_DAGSHUB_TOKEN
```

---

## Training Pipeline

Run model training:

```bash
python main.py
```

Generated artifacts:

```text
Artifacts/
final_model/
```

---

## Run FastAPI

```bash
uvicorn api.app:app --reload
```

Swagger Docs:

```text
http://localhost:8000/docs
```

Health Endpoint:

```text
http://localhost:8000/health
```

---

## Run Streamlit

```bash
streamlit run streamlit_app/app.py
```

UI:

```text
http://localhost:8501
```

---

## Docker

### Build API

```bash
docker build -f Dockerfile.api -t netsec-api .
```

### Run API

```bash
docker run -p 8000:8000 netsec-api
```

### Build Streamlit

```bash
docker build -f Dockerfile.ui -t netsec-ui .
```

### Run Streamlit

```bash
docker run -p 8501:8501 netsec-ui
```

---

## Docker Compose

Run complete application:

```bash
docker compose up --build
```

Services:

| Service   | URL                          |
| --------- | ---------------------------- |
| FastAPI   | http://localhost:8000        |
| Swagger   | http://localhost:8000/docs   |
| Health    | http://localhost:8000/health |
| Streamlit | http://localhost:8501        |

---

## MLflow Tracking

Experiments are tracked using:

* MLflow
* DagsHub

Tracked items:

* Parameters
* Metrics
* Models
* Artifacts

---

## CI/CD Pipeline

GitHub Actions workflow performs:

### Continuous Integration

* Dependency installation
* Ruff linting
* Unit test execution
* Code quality validation

### Continuous Deployment

* Render deployment webhook trigger
* API health verification
* Automated deployment pipeline

Workflow location:

```text
.github/workflows/main.yaml
```

---

## Deployment

### Render Services

#### API Service

* Docker deployment
* FastAPI backend
* Health monitoring

#### UI Service

* Docker deployment
* Streamlit frontend

### Render Blueprint

Infrastructure managed using:

```text
render.yaml
```

---

## API Endpoints

### Health Check

```http
GET /health
```

Response

```json
{
  "status": "healthy"
}
```

### Training

```http
GET /train
```

### Prediction

```http
POST /predict
```

Upload:

```text
CSV File
```

Returns:

```text
Prediction Results
```

---

## Current Production Features

* Modular MLOps architecture
* MongoDB integration
* MLflow experiment tracking
* DagsHub integration
* FastAPI prediction service
* Streamlit UI
* Docker containers
* Docker Compose
* GitHub Actions CI/CD
* Render deployment
* Health monitoring
* Environment variable management
* Model artifact persistence

---

## Future Improvements

### Model Registry

Move model loading from local artifacts to:

* MLflow Model Registry
* DagsHub Model Registry

Benefits:

* Versioned models
* Rollbacks
* Staging/Production promotion

---

### Automated Retraining

Implement:

* Scheduled retraining
* Data drift detection
* Model performance monitoring

---

### Monitoring Stack

Add:

* Prometheus
* Grafana
* OpenTelemetry

Track:

* API latency
* Prediction volume
* Error rates
* Resource utilization

---

### Testing

Expand:

* Unit tests
* Integration tests
* API tests
* Data validation tests

---

### Cloud Infrastructure

Future migration options:

* AWS ECS
* AWS ECR
* AWS S3
* Kubernetes
* Azure Container Apps

---

### Security

Add:

* JWT Authentication
* API Key Management
* Role-Based Access Control
* Secrets Manager Integration

---

### Advanced MLOps

Implement:

* Feature Store
* Model Monitoring
* Data Versioning (DVC)
* Canary Deployments
* Blue-Green Deployments

---

## Learning Outcomes

This project demonstrates practical experience with:

* Machine Learning Engineering
* Production ML Systems
* CI/CD Automation
* Docker
* FastAPI
* Streamlit
* Experiment Tracking
* Model Serving
* Cloud Deployment
* End-to-End MLOps

---


