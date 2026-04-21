# PM Portal

Phase 1 dedicated portal for project readiness intelligence.

## Stack
- Backend: FastAPI (`backend/`)
- Frontend: React + Vite (`frontend/`)

## Quickstart
1. Backend:
   - `cd backend`
   - `python3 -m venv .venv && source .venv/bin/activate`
   - `pip install -r requirements.txt`
   - `uvicorn app.main:app --reload --port 8080`
2. Frontend:
   - `cd frontend`
   - `npm install`
   - `npm run dev`

Set `VITE_API_BASE_URL` if backend is not `http://localhost:8080`.
