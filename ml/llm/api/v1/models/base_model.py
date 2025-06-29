from pydantic import BaseModel, Field

class LLMRequest(BaseModel):
    query: str = Field(..., description="Query for the LLM model")
