from typing import AsyncGenerator

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.models.chat import ChatRequest
from app.services.claude_service import stream_chat

router = APIRouter()


async def _event_stream(request: ChatRequest) -> AsyncGenerator[str, None]:
    async for chunk in stream_chat(request):
        yield f"data: {chunk}\n\n"
    yield "data: [DONE]\n\n"


@router.post("/chat")
async def chat(request: ChatRequest) -> StreamingResponse:
    """Stream AI assistant responses as Server-Sent Events."""
    return StreamingResponse(
        _event_stream(request),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )
