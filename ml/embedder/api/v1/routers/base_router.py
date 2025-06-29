from fastapi import APIRouter, Request
from api.v1.models.base_models import EmbeddingQuery

router = APIRouter()

@router.post("/generate")
async def generate(request: Request, data: EmbeddingQuery):
    embedder = request.app.state.embedder
    embedding = embedder.encode(data.text)
    return {"response": embedding.tolist()}
