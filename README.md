# resume-searcher

Resume Searcher is a system for searching and analyzing resumes using modern ML/LLM models and vector databases.

## Project Structure

- **backend/** — FastAPI microservices for search, resume management, ML and DB integration
- **frontend/** — simple web interface (HTML/JS/CSS)
- **ml/** — services for embedding and LLM response generation
- **datasets/** — datasets for training and testing
- **initdb/** — SQL scripts and data for DB initialization
- **qdrant_migrations/** — migrations for Qdrant

## Quick Start

1. Install Docker and Docker Compose
2. Clone the repository
3. Start all services:
   ```sh
   docker-compose up --build
   ```
4. Frontend will be available at http://localhost:3000 (if you uncomment the frontend in docker-compose)
5. Backend Gateway: http://localhost:8006

## Main Services
- **backend-gateway** — main API (FastAPI)
- **ml-embedder** — embedding generation service
- **ml-llm** — LLM response generation service
- **postgres** — resume database
- **qdrant** — vector database

## API Examples

### Search resumes
POST `/api/v1/search`
```json
{
  "query": "python developer"
}
```

### Get resume by id
GET `/api/v1/resume/{resume_id}`

## Environment Variables (example for backend-gateway)
- `DATABASE_URL` — Postgres connection string
- `QDRANT_URL` — Qdrant address

## Development
- All services can be run separately (see Dockerfile in each service)
- ML services require Python 3.10+, PyTorch, transformers, sentence-transformers

## Authors
- @harnemer Danis Sharafiev

---

A project for searching and analyzing resumes using modern ML and LLM tools.