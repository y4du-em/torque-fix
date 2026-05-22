from enum import Enum

from pydantic import BaseModel, Field

from app.models.diagnosis import DiagnosisResponse
from app.models.vehicle import VehicleContext


class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"


class ChatMessage(BaseModel):
    id: str
    role: MessageRole
    content: str
    created_at: str


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2000)
    history: list[ChatMessage] = Field(default_factory=list, max_length=50)
    vehicle_context: VehicleContext | None = None
    diagnosis_context: DiagnosisResponse | None = None
