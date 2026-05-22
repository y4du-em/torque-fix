import json

from fastapi import APIRouter, HTTPException

from app.models.diagnosis import DiagnosisRequest, DiagnosisResponse
from app.services.claude_service import diagnose_vehicle

router = APIRouter()


@router.post("/diagnose", response_model=DiagnosisResponse)
async def diagnose(request: DiagnosisRequest) -> DiagnosisResponse:
    """Diagnose vehicle issues and return structured repair guidance."""
    try:
        return await diagnose_vehicle(request)
    except json.JSONDecodeError as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Failed to parse diagnosis response from AI service: {exc}",
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred during diagnosis: {exc}",
        ) from exc
