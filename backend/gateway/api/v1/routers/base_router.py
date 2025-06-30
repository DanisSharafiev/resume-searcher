from fastapi import APIRouter, Request
from config.logger import get_logger
from api.v1.models.base_models import SearchRequest

router = APIRouter()

@router.get("/health")
async def health_check(request: Request):
    logger = request.app.state.logger
    logger.info("Health check performed")
    return {"status": "healthy"}

@router.post("/search")
async def search(request: Request, data: SearchRequest):
    logger = request.app.state.logger
    logger.info(f"Search request received with query: {data.query}")
    return {"results": "search results based on the input data"}

@router.get("/resume/{resume_id}")
async def get_resume(request: Request, resume_id: str):
    logger = request.app.state.logger
    logger.info(f"Fetching resume with ID: {resume_id}")
    return {"resume_id": resume_id, "content": "Resume content goes here"}
