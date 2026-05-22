from enum import Enum

from pydantic import BaseModel, Field

from app.models.vehicle import VehicleContext


class DifficultyLevel(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    PROFESSIONAL = "professional"


class PartPriority(str, Enum):
    CRITICAL = "critical"
    RECOMMENDED = "recommended"
    OPTIONAL = "optional"


class Tool(BaseModel):
    name: str
    size: str | None = None
    type: str
    required: bool


class Part(BaseModel):
    name: str
    part_number: str | None = None
    quantity: int
    estimated_cost: str | None = None
    priority: PartPriority


class RepairStep(BaseModel):
    step_number: int
    title: str
    description: str
    warning: str | None = None
    tip: str | None = None
    estimated_time: str | None = None


class DiagnosisRequest(BaseModel):
    vehicle: VehicleContext
    symptoms: list[str] = Field(min_length=1, max_length=20)
    additional_notes: str | None = Field(default=None, max_length=1000)


class DiagnosisResponse(BaseModel):
    id: str
    vehicle: VehicleContext
    symptoms: list[str]
    diagnosis: str
    tools: list[Tool]
    parts: list[Part]
    steps: list[RepairStep]
    difficulty: DifficultyLevel
    estimated_time: str
    estimated_cost: str | None = None
    warning_flags: list[str]
    safety_notes: list[str]
    created_at: str
