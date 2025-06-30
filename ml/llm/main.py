from fastapi import FastAPI, Request
from transformers import AutoTokenizer, AutoModelForCausalLM
from models.llm_model import get_model, get_tokenizer
from api.v1.routers.base_router import router as base_router
import torch
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.tokenizer = get_tokenizer()
    app.state.model = get_model()
    # print(torch.cuda.is_available())
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(router=base_router)
