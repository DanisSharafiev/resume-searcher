from config.config import Config
import psycopg2
# from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance, HnswConfigDiff, HnswConfig
from config.config import EmbedderConfig
import requests
import json

conn = psycopg2.connect(dbname=Config.POSTGRES_DB, user=Config.POSTGRES_USER, password=Config.POSTGRES_PASSWORD, host=Config.POSTGRES_HOST, port=Config.POSTGRES_PORT)
cur = conn.cursor()
cur.execute("SELECT id, text1, text2 FROM items")
rows = cur.fetchall()

# print("Rows fetched from PostgreSQL:")
# for row in rows[:10]:
#     print(row)

def has_collection(client, collection_name):
    try:
        client.get_collection(collection_name)
        return True
    except Exception as e:
        return False

# model = SentenceTransformer('all-MiniLM-L6-v2')
ids, texts1, texts2 = zip(*rows)

client = QdrantClient(host=Config.QDRANT_HOST, port=Config.QDRANT_PORT)
if not has_collection(client, "first_collection"):
    print("Creating first collection...")
    # embeddings1 = model.encode(texts1)
    embeddings1 = []
    for text in texts1:
        embedding = requests.post(
            EmbedderConfig.get_connection_string() + "/generate",
            json={"text": text}
        ).json()
        embedding = embedding["response"]
        embedding = json.loads(embedding)
    # print(embeddings1)
    client.recreate_collection(
        collection_name="first_collection",
        # vectors_config={"size": len(embeddings1[0]), "distance": "Cosine"},
        vectors_config=VectorParams(size=len(embeddings1[0]), 
                                    distance=Distance.COSINE,
                                    hnsw_config=HnswConfigDiff(
                                        m=16,
                                        ef_construct=200,
                                        full_scan_threshold=1000
                                    )),
    )
    client.upsert(
        collection_name="first_collection",
        points=[
            PointStruct(id=id_, vector=embedding)
            for id_, embedding in zip(ids, embeddings1)
        ],
    )
if not has_collection(client, "second_collection"):
    print("Creating second collection...")
    embeddings2 = model.encode(texts2)
    print(embeddings2)
    client.recreate_collection(
        collection_name="second_collection",
        vectors_config=VectorParams(size=len(embeddings1[0]), 
                                    distance=Distance.COSINE,
                                    hnsw_config=HnswConfigDiff(
                                        m=16,
                                        ef_construct=200,
                                        full_scan_threshold=1000
                                    )),
    )
    client.upsert(
        collection_name="second_collection",
        points=[
            PointStruct(id=id_, vector=embedding)
            for id_, embedding in zip(ids, embeddings2)
        ],
    )
    
print("Collections created and data uploaded successfully.")

# print("\nFirst collection points (первые 5):")
# points = client.scroll(
#     collection_name="first_collection",
#     limit=5,
#     with_vectors=True,
# )[0]
# for point in points:
#     print(f"id: {point.id}, vector[:5]: {point.vector[:5]}...")

# print("\nSecond collection points (первые 5):")
# points = client.scroll(
#     collection_name="second_collection",
#     limit=5,
#     with_vectors=True,
# )[0]
# for point in points:
#     print(f"id: {point.id}, vector[:5]: {point.vector[:5]}...")