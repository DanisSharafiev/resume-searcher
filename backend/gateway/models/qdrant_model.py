from config.config import QdrantConfig
from qdrant_client import QdrantClient

class QdrantModel:
    def __init__(self):
        self.client = QdrantClient(
            url=f"http://{QdrantConfig.HOST}:{QdrantConfig.PORT}"
        )

    def search(self, query, limit=10, collection_name="first_collection"):
        response = self.client.search(collection_name=collection_name, query_vector=query, limit=limit)
        response.sort(key=lambda x: x.score, reverse=True)
        result = []
        for point in response:
            result.append(point.id)
        return result
