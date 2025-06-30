# Use official Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt ./

RUN pip install uv
RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install --system -r requirements.txt

# RUN pip install --no-cache-dir -r requirements.txt

# Pre-download the model to cache it in the image
# RUN python -c "from transformers import AutoTokenizer, AutoModelForCausalLM; \
#     model_name = 'microsoft/phi-3-mini-4k-instruct'; \
#     AutoTokenizer.from_pretrained(model_name, trust_remote_code=True); \
#     AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=True)"

# Copy application code
COPY . .

# Expose port (adjust if needed)
EXPOSE 8000

# Start the application (adjust if needed)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
