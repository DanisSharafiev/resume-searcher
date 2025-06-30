class PostgresConfig:
    HOST = "localhost"
    PORT = 5434
    USER = "resume_user"
    PASSWORD = "resume_password"
    DB = "resume_db"

class QdrantConfig:
    HOST = "localhost"
    PORT = 6333

class LLMConfig:
    HOST = "localhost"
    PORT = 8000

    @classmethod
    def get_connection_string(cls) -> str:
        return f"http://{cls.HOST}:{cls.PORT}"