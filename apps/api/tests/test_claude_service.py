import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.models.chat import ChatMessage, ChatRequest, MessageRole
from app.models.diagnosis import DiagnosisRequest, DifficultyLevel
from app.models.vehicle import FuelType, VehicleContext, VehicleType
from app.services.claude_service import diagnose_vehicle, stream_chat


@pytest.fixture
def diagnosis_request(sample_vehicle_context) -> DiagnosisRequest:
    return DiagnosisRequest(
        vehicle=sample_vehicle_context,
        symptoms=["Engine won't start", "Rough idling"],
    )


@pytest.fixture
def chat_request(sample_vehicle_context) -> ChatRequest:
    return ChatRequest(
        message="What tools do I need?",
        history=[],
        vehicle_context=sample_vehicle_context,
    )


class TestDiagnoseVehicle:
    async def test_returns_diagnosis_response_from_claude_json(
        self, diagnosis_request, sample_claude_json
    ):
        # Arrange
        mock_block = MagicMock()
        mock_block.type = "text"
        mock_block.text = sample_claude_json

        mock_message = MagicMock()
        mock_message.content = [mock_block]

        with patch("app.services.claude_service._sync_client") as mock_client:
            mock_client.messages.create.return_value = mock_message

            # Act
            result = await diagnose_vehicle(diagnosis_request)

        # Assert
        assert result.diagnosis == "Faulty spark plug causing ignition failure."
        assert result.difficulty == DifficultyLevel.EASY
        assert result.estimated_time == "30 minutes"
        assert result.estimated_cost == "₹150-₹250"
        assert len(result.tools) == 2
        assert len(result.parts) == 1
        assert len(result.steps) == 1

    async def test_maps_tool_fields_correctly(self, diagnosis_request, sample_claude_json):
        # Arrange
        mock_block = MagicMock()
        mock_block.type = "text"
        mock_block.text = sample_claude_json

        mock_message = MagicMock()
        mock_message.content = [mock_block]

        with patch("app.services.claude_service._sync_client") as mock_client:
            mock_client.messages.create.return_value = mock_message

            # Act
            result = await diagnose_vehicle(diagnosis_request)

        # Assert
        required_tool = next(t for t in result.tools if t.required)
        assert required_tool.name == "Spark plug wrench"
        assert required_tool.size == "16mm"
        assert required_tool.type == "socket wrench"

    async def test_maps_part_fields_correctly(self, diagnosis_request, sample_claude_json):
        # Arrange
        mock_block = MagicMock()
        mock_block.type = "text"
        mock_block.text = sample_claude_json

        mock_message = MagicMock()
        mock_message.content = [mock_block]

        with patch("app.services.claude_service._sync_client") as mock_client:
            mock_client.messages.create.return_value = mock_message

            # Act
            result = await diagnose_vehicle(diagnosis_request)

        # Assert
        part = result.parts[0]
        assert part.name == "NGK Spark Plug"
        assert part.part_number == "CR7HSA"
        assert part.quantity == 1
        assert part.priority.value == "critical"

    async def test_maps_step_fields_correctly(self, diagnosis_request, sample_claude_json):
        # Arrange
        mock_block = MagicMock()
        mock_block.type = "text"
        mock_block.text = sample_claude_json

        mock_message = MagicMock()
        mock_message.content = [mock_block]

        with patch("app.services.claude_service._sync_client") as mock_client:
            mock_client.messages.create.return_value = mock_message

            # Act
            result = await diagnose_vehicle(diagnosis_request)

        # Assert
        step = result.steps[0]
        assert step.step_number == 1
        assert step.title == "Remove spark plug"
        assert step.warning == "Ensure engine is cold before starting."
        assert step.tip == "Mark the plug wire to avoid confusion."
        assert step.estimated_time == "10 minutes"

    async def test_assigns_uuid_and_timestamp(self, diagnosis_request, sample_claude_json):
        # Arrange
        mock_block = MagicMock()
        mock_block.type = "text"
        mock_block.text = sample_claude_json
        mock_message = MagicMock()
        mock_message.content = [mock_block]

        with patch("app.services.claude_service._sync_client") as mock_client:
            mock_client.messages.create.return_value = mock_message

            # Act
            result = await diagnose_vehicle(diagnosis_request)

        # Assert
        assert result.id  # non-empty UUID
        assert result.created_at  # non-empty ISO timestamp

    async def test_raises_on_invalid_json(self, diagnosis_request):
        # Arrange
        mock_block = MagicMock()
        mock_block.type = "text"
        mock_block.text = "not valid json at all"
        mock_message = MagicMock()
        mock_message.content = [mock_block]

        with patch("app.services.claude_service._sync_client") as mock_client:
            mock_client.messages.create.return_value = mock_message

            # Act / Assert
            with pytest.raises(json.JSONDecodeError):
                await diagnose_vehicle(diagnosis_request)

    async def test_raises_on_non_text_content_block(self, diagnosis_request):
        # Arrange
        mock_block = MagicMock()
        mock_block.type = "tool_use"
        mock_message = MagicMock()
        mock_message.content = [mock_block]

        with patch("app.services.claude_service._sync_client") as mock_client:
            mock_client.messages.create.return_value = mock_message

            # Act / Assert
            with pytest.raises(ValueError, match="Unexpected content block type"):
                await diagnose_vehicle(diagnosis_request)


class TestStreamChat:
    async def test_yields_text_chunks_from_async_stream(self, chat_request):
        # Arrange
        async def _fake_text_stream():
            for chunk in ["Hello", " world", "!"]:
                yield chunk

        mock_stream_ctx = AsyncMock()
        mock_stream_ctx.__aenter__ = AsyncMock(return_value=mock_stream_ctx)
        mock_stream_ctx.__aexit__ = AsyncMock(return_value=False)
        mock_stream_ctx.text_stream = _fake_text_stream()

        with patch("app.services.claude_service._async_client") as mock_client:
            mock_client.messages.stream.return_value = mock_stream_ctx

            # Act
            chunks = [chunk async for chunk in stream_chat(chat_request)]

        # Assert
        assert chunks == ["Hello", " world", "!"]

    async def test_passes_history_to_claude(self, sample_vehicle_context):
        # Arrange
        history = [
            ChatMessage(id="1", role=MessageRole.USER, content="hi", created_at="2024-01-01T00:00:00Z"),
            ChatMessage(id="2", role=MessageRole.ASSISTANT, content="hello", created_at="2024-01-01T00:00:00Z"),
        ]
        request = ChatRequest(message="What next?", history=history, vehicle_context=sample_vehicle_context)

        async def _empty_stream():
            return
            yield  # make it an async generator

        mock_stream_ctx = AsyncMock()
        mock_stream_ctx.__aenter__ = AsyncMock(return_value=mock_stream_ctx)
        mock_stream_ctx.__aexit__ = AsyncMock(return_value=False)
        mock_stream_ctx.text_stream = _empty_stream()

        with patch("app.services.claude_service._async_client") as mock_client:
            mock_client.messages.stream.return_value = mock_stream_ctx

            # Act
            _ = [chunk async for chunk in stream_chat(request)]

            # Assert — all history messages + new user message are sent
            call_kwargs = mock_client.messages.stream.call_args.kwargs
            assert len(call_kwargs["messages"]) == 3
            assert call_kwargs["messages"][2]["content"] == "What next?"
