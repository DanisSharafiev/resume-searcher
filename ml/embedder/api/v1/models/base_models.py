from pydantic import BaseModel, Field

class EmbeddingQuery(BaseModel):
    text: str = Field(..., description="Text for embedding creator")
