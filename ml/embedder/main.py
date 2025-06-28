from fastapi import FastAPI
from config.logger import get_logger
from models.embedder import Embedder

def lifespan(app: FastAPI):
    app.state.logger = get_logger()
    app.state.logger.info("Application startup")
    app.state.embedder = Embedder(app.state.logger)
    yield
    app.state.logger.info("Application shutdown")

app = FastAPI(lifespan=lifespan)