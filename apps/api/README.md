# TorqueFix API

FastAPI backend providing AI-powered vehicle diagnosis and repair guidance.

## Setup

```bash
cd apps/api

# Create virtual environment
python3.12 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"

# Configure environment
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY

# Start dev server
uvicorn app.main:app --reload --port 8000
```

## Endpoints

- `GET /health` — Health check
- `POST /api/v1/diagnose` — Diagnose vehicle issues (returns JSON)
- `POST /api/v1/chat` — Stream AI assistant response (SSE)

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `ANTHROPIC_API_KEY` | required | Your Anthropic API key |
| `MODEL_NAME` | `claude-sonnet-4-20250514` | Claude model to use |
| `MAX_TOKENS` | `4096` | Max tokens for responses |
| `CORS_ORIGINS` | `["http://localhost:3000"]` | Allowed CORS origins |
| `ENVIRONMENT` | `development` | Runtime environment |
