from config.config import Config
import psycopg2
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance, HnswConfigDiff, HnswConfig
from config.config import EmbedderConfig
import requests
import json
import time

for _ in range(60):
    try:
        conn = psycopg2.connect(dbname=Config.POSTGRES_DB, user=Config.POSTGRES_USER, password=Config.POSTGRES_PASSWORD, host=Config.POSTGRES_HOST, port=Config.POSTGRES_PORT)
        break
    except Exception as e:
        time.sleep(5)
        print("Retrying connection to postgres...")

cur = conn.cursor()
cur.execute("SELECT id, text1, text2 FROM items")
rows = cur.fetchall()

def has_collection(client, collection_name):
    try:
        client.get_collection(collection_name)
        return True
    except Exception as e:
        return False

ids, texts1, texts2 = zip(*rows)
for _ in range(60):
    try:
        client = QdrantClient(host=Config.QDRANT_HOST, port=Config.QDRANT_PORT)
        break
    except Exception as e:
        time.sleep(5)
        print("Retrying connection to Qdrant...")

for _ in range(60):
    embedding = requests.post(
            EmbedderConfig.get_connection_string() + "/generate",
            json={"text": "test text for embedding generation"}
        ).json()
    if "response" in embedding:
        embedding = embedding["response"]
        embedding = json.loads(embedding)
        break
    else:
        time.sleep(5)
        print("Retrying embedding generation...")

if not has_collection(client, "first_collection"):
    print("Creating first collection...")
    embeddings1 = []
    embedding = requests.post(
            EmbedderConfig.get_connection_string() + "/generate",
            json={"text": "text"}
        ).json()
    embedding = embedding["response"]
    embedding = json.loads(embedding)
    client.recreate_collection(
        collection_name="first_collection",
        vectors_config=VectorParams(size=len(embedding), 
                                    distance=Distance.COSINE,
                                    hnsw_config=HnswConfigDiff(
                                        m=16,
                                        ef_construct=200,
                                        full_scan_threshold=1000
                                    )),
    )
    for id_, text in zip(ids[:5000], texts1[:5000]):
        embedding = requests.post(
            EmbedderConfig.get_connection_string() + "/generate",
            json={"text": text}
        ).json()
        embedding = embedding["response"]
        embedding = json.loads(embedding)
        embeddings1.append(embedding)
        client.upsert(
            collection_name="first_collection",
            points=[PointStruct(id=id_, vector=embedding)],
        )
    # for id_, embedding in zip(ids, embeddings1):
    #     client.upsert(
    #         collection_name="first_collection",
    #         points=[PointStruct(id=id_, vector=embedding)],
    #     )
# if not has_collection(client, "second_collection"):
#     print("Creating second collection...")
#     embeddings2 = []
#     for text in texts1:
#         embedding = requests.post(
#             EmbedderConfig.get_connection_string() + "/generate",
#             json={"text": text}
#         ).json()
#         embedding = embedding["response"]
#         embedding = json.loads(embedding)
#         embeddings2.append(embedding)
#     print(embeddings2)
#     client.recreate_collection(
#         collection_name="second_collection",
#         vectors_config=VectorParams(size=len(embeddings1[0]), 
#                                     distance=Distance.COSINE,
#                                     hnsw_config=HnswConfigDiff(
#                                         m=16,
#                                         ef_construct=200,
#                                         full_scan_threshold=1000
#                                     )),
#     )
#     client.upsert(
#         collection_name="second_collection",
#         points=[
#             PointStruct(id=id_, vector=embedding)
#             for id_, embedding in zip(ids, embeddings2)
#         ],
#     )
    
print("Collections created and data uploaded successfully.")
