class PostgresConfig:
    def __init__(self, host: str, port: int, user: str, password: str, database: str):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database

    def get_connection_string(self) -> str:
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"

class QdrantConfig:
    def __init__(self, host: str, port: int, user: str, password: str, database: str):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database

    def get_connection_string(self) -> str:
        return f"qd://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"

class LLMConfig:
    def __init__(self, hostname: str, port: int):
        self.port = port
        self.hostname = hostname

    def get_connection_string(self) -> str:
        return f"http://{self.hostname}:{self.port}"