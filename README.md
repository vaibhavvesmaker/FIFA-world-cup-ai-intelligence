# FIFA World Cup AI Intelligence

An AI-powered football intelligence platform combining live match data, machine-learning win probabilities, historical World Cup analytics, and cited conversational answers.

## Product pillars

1. **Live Match Intelligence** — ingest match events and preserve a timestamped probability timeline.
2. **Historical Match Explorer** — browse tournaments, teams, players, matches, and event histories.
3. **World Cup Copilot** — answer questions through structured database tools and cited retrieval-augmented generation (RAG).
4. **Historical Match Twin** — find past matches most similar to the current live state.

## Current milestone: Foundation

The first working component is a small FastAPI service with typed configuration and a health endpoint. API credentials are optional at this stage and must never be committed.

### Run locally

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp ../.env.example ../.env
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/health`. Expected response:

```json
{"status":"ok","service":"FIFA World Cup AI Intelligence API","environment":"development"}
```

Run the tests:

```bash
cd backend
pytest
```

### Run the frontend

Keep the backend running, then open a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:3000`. The header reports **Backend online** only when
the browser receives a successful response from the FastAPI `/health` endpoint.

## Planned architecture

```text
Live/Historical Data -> Validation -> PostgreSQL -> Analytics/ML -> API -> Web App
                                      |              |
                                      +-> pgvector <-+-> AI Copilot
```

## Repository structure

```text
backend/       FastAPI, ingestion, analytics, ML, and AI orchestration
docs/          Product decisions, data contracts, and model documentation
frontend/      Next.js application (next milestone)
```

## Data and AI principles

- Structured statistics are calculated with database queries, not guessed by an LLM.
- Narrative questions use RAG with visible sources.
- Every live prediction is stored with event time, ingestion time, model version, and inputs.
- The interface must disclose stale or unavailable data.
- Generated explanations must remain traceable to retrieved data and model features.

## Security

Keep secrets in `.env` locally and protected environment variables in deployment. The committed `.env.example` contains names only.

## License

MIT
