from pydantic import BaseModel, Field

class SearchRequest(BaseModel):
    query: str = Field(..., description="Query for search")
