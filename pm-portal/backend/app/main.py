from __future__ import annotations

from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .models import RecommendationDecision
from .service import build_standup_view, set_decision

app = FastAPI(title="PM Portal API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class DecisionUpdate(BaseModel):
    state: str
    rationale: str = ""
    owner: str = ""
    due_date: str = ""


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/standup")
def get_standup() -> dict:
    return build_standup_view().model_dump(mode="json")


@app.get("/api/projects/{project_name}")
def get_project(project_name: str) -> dict:
    run = build_standup_view()
    for project in run.projects:
        if project.project.name.lower() == project_name.lower():
            return project.model_dump(mode="json")
    raise HTTPException(status_code=404, detail="Project not found")


@app.post("/api/recommendations/{recommendation_id}/decision")
def update_decision(recommendation_id: str, payload: DecisionUpdate) -> dict:
    if payload.state not in {"approved", "rejected", "defer", "pending"}:
        raise HTTPException(status_code=400, detail="Invalid decision state")
    decision = RecommendationDecision(
        recommendation_id=recommendation_id,
        state=payload.state,
        rationale=payload.rationale,
        owner=payload.owner,
        due_date=payload.due_date,
        updated_at=datetime.now(timezone.utc),
    )
    set_decision(recommendation_id, decision)
    return {"ok": True, "decision": decision.model_dump(mode="json")}
