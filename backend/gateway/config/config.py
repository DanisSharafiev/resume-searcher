class PostgresConfig:
    HOST = "postgres"
    PORT = 5432
    USER = "resume_user"
    PASSWORD = "resume_password"
    DB = "resume_db"

class QdrantConfig:
    HOST = "qdrant"
    PORT = 6333

class LLMConfig:
    HOST = "ml-llm"
    PORT = 8002

    @classmethod
    def get_connection_string(cls) -> str:
        return f"http://{cls.HOST}:{cls.PORT}"

class EmbedderConfig:
    HOST = "ml-embedder"
    PORT = 8001

    @classmethod
    def get_connection_string(cls) -> str:
        return f"http://{cls.HOST}:{cls.PORT}"
