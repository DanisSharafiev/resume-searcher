FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements if exists, else install manually
COPY requirements.txt ./
# RUN pip install --no-cache-dir -r requirements.txt
RUN pip install uv
RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install --system -r requirements.txt
#     pip install --no-cache-dir psycopg2-binary sentence-transformers qdrant-client


# Copy application code
COPY . .

CMD ["python", "main.py"]
