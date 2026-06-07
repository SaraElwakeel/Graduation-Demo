"""
Guardian Eye — Pydantic Schemas
All request/response contracts matching DEMO_APP.md §5 exactly.
"""

from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, Field
import datetime


# ── Shared sub-schemas ────────────────────────────────────────────────────────

class GateWeights(BaseModel):
    skeleton: float = Field(..., ge=0.0, le=1.0)
    interaction: float = Field(..., ge=0.0, le=1.0)
    object: float = Field(..., ge=0.0, le=1.0)
    vit: float = Field(..., ge=0.0, le=1.0)


class GQSScores(BaseModel):
    q_skel: float = Field(..., ge=0.0, le=1.0)
    q_int: float = Field(..., ge=0.0, le=1.0)
    q_obj: float = Field(..., ge=0.0, le=1.0)
    q_po: float = Field(..., ge=0.0, le=1.0)
    valid_ratio: float = Field(..., ge=0.0, le=1.0)


class WeaponInfo(BaseModel):
    flag: bool
    cls: Optional[str] = None


class Telemetry(BaseModel):
    """Geometry-derived heuristics — NOT classifier outputs."""
    people: int
    peak_window: list[int] = Field(..., min_length=2, max_length=2)
    weapon: WeaponInfo


# ── /predict ──────────────────────────────────────────────────────────────────

class PredictResponse(BaseModel):
    verdict: str
    confidence: float
    threshold: float
    gate: GateWeights
    gqs: GQSScores
    telemetry: Telemetry
    clip_id: str


# ── /explain ──────────────────────────────────────────────────────────────────

class ExplainRequest(BaseModel):
    clip_id: str
    language: str = Field(default="en", pattern="^(en|ar)$")


class ExplainResponse(BaseModel):
    narrative: str
    incident_id: str
    language: str


# ── /history ──────────────────────────────────────────────────────────────────

class IncidentSummary(BaseModel):
    incident_id: str
    timestamp: datetime.datetime
    source: str
    verdict: str
    confidence: float
    thumbnail: Optional[str] = None
    overlay: Optional[str] = None          # NEW — skeleton-overlay video path
    people_count: int
    weapon_flag: bool
    weapon_class: Optional[str] = None
    peak_window: list[int]
    narrative_preview: Optional[str] = None


class HistoryResponse(BaseModel):
    total: int
    incidents: list[IncidentSummary]


# ── /ask ──────────────────────────────────────────────────────────────────────

class AskRequest(BaseModel):
    question: str = Field(..., min_length=1)
    language: str = Field(default="en", pattern="^(en|ar)$")


class AskResponse(BaseModel):
    answer: str
    incidents: list[IncidentSummary]
    language: str
