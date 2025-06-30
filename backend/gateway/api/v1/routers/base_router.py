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
    postgres = request.app.state.postgres_model
    resume = postgres.fetch_from_id(resume_id)
    logger.info(f"Resume fetched: {resume}")
    full_resume = resume[1] + resume[2]
    llm_model = request.app.state.llm_model
    llm_response = llm_model.get_response(full_resume)
    json_maker = request.app.state.json_maker
    llm_response_markdown = json_maker.make_llm_response(llm_response["data"]["text"], full_resume)
    return {"resume_id": resume_id, "content": llm_response_markdown}

