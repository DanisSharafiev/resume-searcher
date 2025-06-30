from fastapi import FastAPI
from config.config import Config
from config.logger import get_logger
from api.v1.routers.base_router import router as base_router
from models.postgres_model import PostgresModel
from models.llm_model import LLMModel
from models.json_builder import JsonMaker

async def lifespan(app: FastAPI):
    app.state.logger = get_logger()
    app.state.logger.info("Application startup")
    app.state.postgres_model = PostgresModel(
        dbname=Config.POSTGRES_DB,
        user=Config.POSTGRES_USER,
        password=Config.POSTGRES_PASSWORD,
        host=Config.POSTGRES_HOST,
        port=Config.POSTGRES_PORT
    )
    app.state.logger.info("Postgres model initialized")
    app.state.llm_model = LLMModel()
    app.state.logger.info("LLM model initialized")
    app.state.json_maker = JsonMaker()
    yield
    app.state.logger.info("Application shutdown")

app = FastAPI(lifespan=lifespan)
app.include_router(base_router, prefix="/api/v1")
