from fastapi import APIRouter, Request
from fastapi.responses import Response
from config.logger import get_logger
from api.v1.models.base_models import SearchRequest
from config.config import EmbedderConfig
import requests
import json

router = APIRouter()

@router.get("/health")
async def health_check(request: Request):
    logger = request.app.state.logger
    logger.info("Health check performed")
    return {"status": "healthy"}

@router.options("/resume/{resume_id}")
async def resume_options(resume_id: str):
    return Response(
        status_code=200,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
        }
    )

@router.post("/search")
async def search(request: Request, data: SearchRequest):
    logger = request.app.state.logger
    logger.info(f"Search request received with query: {data.query}")
    qdrant_model = request.app.state.qdrant_model
    logger.info(f"Embedder connection string: {EmbedderConfig.get_connection_string()}/generate")
    embedding = requests.post(
        EmbedderConfig.get_connection_string() + "/generate",
        json={"text": data.query}
    ).json()
    embedding = embedding["response"]
    logger.info(f"Embedding generated: {embedding}")
    embedding = json.loads(embedding)
    ids = qdrant_model.search(collection_name="first_collection", query=embedding, limit=10)
    postgres_model = request.app.state.postgres_model
    result = []
    for id in ids:
        # Position : positionName, Experience : experience years, Age : age years old
        additional_info = postgres_model.fetch_position_experience_age(id)
        result.append({"id": id, "name": additional_info[0], "position": f"{additional_info[1]} years of experience, {additional_info[2]} years old"})
    return {"results": result}

@router.get("/resume/{resume_id}")
async def get_resume(request: Request, resume_id: str):
    try:
        logger = request.app.state.logger
        logger.info(f"Fetching resume with ID: {resume_id}")
        postgres = request.app.state.postgres_model
        resume = postgres.fetch_from_id(resume_id)
        logger.info(f"Resume fetched: {resume}")
        
        if not resume:
            logger.error(f"Resume with ID {resume_id} not found")
            return {"error": "Resume not found"}
            
        full_resume = resume[1] + resume[2]
        llm_model = request.app.state.llm_model
        # llm_response = llm_model.get_response(full_resume)
        llm_response = {"data": "Sample LLM response based on the resume content"}
        json_maker = request.app.state.json_maker
        llm_response_markdown = json_maker.make_llm_response(llm_response["data"], full_resume)
        return {"resume_id": resume_id, "content": llm_response_markdown}
    except Exception as e:
        logger.error(f"Error fetching resume {resume_id}: {str(e)}")
        return {"error": f"Error fetching resume: {str(e)}"}
