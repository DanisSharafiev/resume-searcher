class Config:
    POSTGRES_HOST = "postgres"
    POSTGRES_PORT = 5432
    POSTGRES_USER = "resume_user"
    POSTGRES_PASSWORD = "resume_password"
    POSTGRES_DB = "resume_db"
    QDRANT_HOST = "qdrant"
    QDRANT_PORT = 6333
    
class EmbedderConfig:
    HOST = "ml-embedder"
    PORT = 8001

    @classmethod
    def get_connection_string(cls) -> str:
        return f"http://{cls.HOST}:{cls.PORT}"
