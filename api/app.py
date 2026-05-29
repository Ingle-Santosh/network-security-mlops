from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from network_security_mlops.utils.logger import logger
from network_security_mlops.utils.io_utils import load_object
from network_security_mlops.utils.ml_utils.model.estimator import NetworkModel

from api.routers import health, train, predict


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ── startup: load model once ──────────────────────────────────────
    logger.info("Loading model and preprocessor...")
    app.state.model = NetworkModel(
        preprocessor=load_object(Path("final_model") / "preprocessor.joblib"),
        model=load_object(Path("final_model") / "model.joblib"),
    )
    logger.info("Model loaded successfully")
    yield
    # ── shutdown ──────────────────────────────────────────────────────
    logger.info("Shutting down")


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(train.router)
app.include_router(predict.router)
