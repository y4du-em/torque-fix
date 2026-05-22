import json
import uuid
from datetime import UTC, datetime
from typing import AsyncGenerator

import anthropic

from app.config import settings
from app.models.chat import ChatRequest
from app.models.diagnosis import (
    DiagnosisRequest,
    DiagnosisResponse,
    DifficultyLevel,
    Part,
    PartPriority,
    RepairStep,
    Tool,
)
from app.prompts.assistant_prompt import build_assistant_system_prompt
from app.prompts.diagnosis_prompt import (
    build_diagnosis_system_prompt,
    build_diagnosis_user_prompt,
)

_sync_client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
_async_client = anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key)


async def diagnose_vehicle(request: DiagnosisRequest) -> DiagnosisResponse:
    system_prompt = build_diagnosis_system_prompt()
    user_prompt = build_diagnosis_user_prompt(
        vehicle=request.vehicle,
        symptoms=request.symptoms,
        notes=request.additional_notes,
    )

    import asyncio

    def _call_claude() -> str:
        message = _sync_client.messages.create(
            model=settings.model_name,
            max_tokens=settings.max_tokens,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )
        block = message.content[0]
        if block.type != "text":
            raise ValueError("Unexpected content block type from Claude")
        return block.text

    raw_json = await asyncio.to_thread(_call_claude)
    data = json.loads(raw_json)

    tools = [
        Tool(
            name=t["name"],
            size=t.get("size"),
            type=t["type"],
            required=t["required"],
        )
        for t in data.get("tools", [])
    ]

    parts = [
        Part(
            name=p["name"],
            part_number=p.get("partNumber"),
            quantity=p["quantity"],
            estimated_cost=p.get("estimatedCost"),
            priority=PartPriority(p["priority"]),
        )
        for p in data.get("parts", [])
    ]

    steps = [
        RepairStep(
            step_number=s["stepNumber"],
            title=s["title"],
            description=s["description"],
            warning=s.get("warning"),
            tip=s.get("tip"),
            estimated_time=s.get("estimatedTime"),
        )
        for s in data.get("steps", [])
    ]

    return DiagnosisResponse(
        id=str(uuid.uuid4()),
        vehicle=request.vehicle,
        symptoms=request.symptoms,
        diagnosis=data["diagnosis"],
        tools=tools,
        parts=parts,
        steps=steps,
        difficulty=DifficultyLevel(data["difficulty"]),
        estimated_time=data["estimatedTime"],
        estimated_cost=data.get("estimatedCost"),
        warning_flags=data.get("warningFlags", []),
        safety_notes=data.get("safetyNotes", []),
        created_at=datetime.now(UTC).isoformat(),
    )


async def stream_chat(request: ChatRequest) -> AsyncGenerator[str, None]:
    system_prompt = build_assistant_system_prompt(
        vehicle=request.vehicle_context,
        diagnosis=request.diagnosis_context,
    )

    messages = [
        {"role": msg.role.value, "content": msg.content}
        for msg in request.history
    ]
    messages.append({"role": "user", "content": request.message})

    async with _async_client.messages.stream(
        model=settings.model_name,
        max_tokens=settings.max_tokens,
        system=system_prompt,
        messages=messages,
    ) as stream:
        async for text in stream.text_stream:
            yield text
