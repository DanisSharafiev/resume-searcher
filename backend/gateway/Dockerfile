# syntax=docker/dockerfile:1
FROM python:3.9

WORKDIR /app

COPY requirements.txt .

# RUN pip install uv
# RUN --mount=type=cache,target=/root/.cache/uv \
#     uv pip install --system -r requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]