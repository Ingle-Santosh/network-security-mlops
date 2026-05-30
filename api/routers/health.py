from fastapi import APIRouter
from starlette.responses import RedirectResponse

router = APIRouter(tags=["health"])

@router.get("/health")
async def health_check():
    return {"status": "healthy"}

@router.get("/")
async def index():
    return RedirectResponse(url="/docs")