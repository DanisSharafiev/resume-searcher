from config.config import Config
import psycopg2
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient

conn = psycopg2.connect(dbname=Config.POSTGRES_DB, user=Config.POSTGRES_USER, password=Config.POSTGRES_PASSWORD, host=Config.POSTGRES_HOST, port=Config.POSTGRES_PORT)
cur = conn.cursor()
cur.execute("SELECT id, text1, text2 FROM items")
rows = cur.fetchall()

print("Rows fetched from PostgreSQL:")
for row in rows[:10]:
    print(row)

model = SentenceTransformer('all-MiniLM-L6-v2')
ids, texts1, texts2 = zip(*rows)

client = QdrantClient(host=Config.QDRANT_HOST, port=Config.QDRANT_PORT)
if not client.has_collection("first_collection"):  
    embeddings = model.encode(texts1)
    client.recreate_collection(
        collection_name="first_collection",
        vectors_config={"size": len(embeddings[0]), "distance": "Cosine"},
    )
    client.upload_collection(
        collection_name="first_collection",
        points=[
            {"id": str(id_), "vector": embedding}
            for id_, embedding in zip(ids, embeddings)
        ],
    )
if not client.has_collection("second_collection"):
    embeddings = model.encode(texts2)
    client.recreate_collection(
        collection_name="second_collection",
        vectors_config={"size": len(embeddings[0]), "distance": "Cosine"},
    )
    client.upload_collection(
        collection_name="second_collection",
        points=[
            {"id": str(id_), "vector": embedding}
            for id_, embedding in zip(ids, embeddings)
        ],
    )
    

