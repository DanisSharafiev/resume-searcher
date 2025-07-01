from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.config import PostgresConfig
from config.logger import get_logger
from api.v1.routers.base_router import router as base_router
from models.postgres_model import PostgresModel
from models.llm_model import LLMModel
from models.json_builder import JsonMaker
from models.qdrant_model import QdrantModel

async def lifespan(app: FastAPI):
    app.state.logger = get_logger()
    app.state.logger.info("Application startup")
    app.state.postgres_model = PostgresModel(
        dbname=PostgresConfig.DB,
        user=PostgresConfig.USER,
        password=PostgresConfig.PASSWORD,
        host=PostgresConfig.HOST,
        port=PostgresConfig.PORT
    )
    app.state.logger.info("Postgres model initialized")
    app.state.llm_model = LLMModel()
    app.state.logger.info("LLM model initialized")
    app.state.qdrant_model = QdrantModel()
    app.state.json_maker = JsonMaker()
    yield
    app.state.logger.info("Application shutdown")

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(base_router, prefix="/api/v1")
