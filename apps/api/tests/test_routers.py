import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from app.models.diagnosis import DiagnosisResponse, DifficultyLevel
from app.models.vehicle import FuelType, VehicleContext, VehicleType


def _make_diagnosis_response(vehicle: dict) -> DiagnosisResponse:
    return DiagnosisResponse(
        id="test-uuid",
        vehicle=VehicleContext(**vehicle),
        symptoms=["Engine noise"],
        diagnosis="Faulty spark plug.",
        tools=[],
        parts=[],
        steps=[],
        difficulty=DifficultyLevel.EASY,
        estimated_time="30 minutes",
        warning_flags=[],
        safety_notes=["Wear gloves."],
        created_at="2024-01-01T00:00:00Z",
    )


class TestHealthEndpoint:
    def test_returns_ok(self, client: TestClient):
        # Act
        response = client.get("/health")

        # Assert
        assert response.status_code == 200
        assert response.json() == {"status": "ok", "service": "torquefix-api"}


class TestDiagnoseEndpoint:
    def test_returns_diagnosis_on_success(self, client: TestClient, sample_diagnosis_payload: dict):
        # Arrange
        mock_response = _make_diagnosis_response(sample_diagnosis_payload["vehicle"])

        with patch("app.routers.diagnosis.diagnose_vehicle", return_value=mock_response):
            # Act
            response = client.post("/api/v1/diagnose", json=sample_diagnosis_payload)

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "test-uuid"
        assert data["diagnosis"] == "Faulty spark plug."
        assert data["difficulty"] == "easy"

    def test_returns_422_for_invalid_request(self, client: TestClient):
        # Arrange — missing required fields
        payload = {"vehicle": {"make": "Honda"}}

        # Act
        response = client.post("/api/v1/diagnose", json=payload)

        # Assert
        assert response.status_code == 422

    def test_returns_422_for_empty_symptoms(self, client: TestClient, sample_vehicle: dict):
        # Arrange
        payload = {"vehicle": sample_vehicle, "symptoms": []}

        # Act
        response = client.post("/api/v1/diagnose", json=payload)

        # Assert
        assert response.status_code == 422

    def test_returns_502_when_claude_returns_invalid_json(
        self, client: TestClient, sample_diagnosis_payload: dict
    ):
        # Arrange
        with patch(
            "app.routers.diagnosis.diagnose_vehicle",
            side_effect=json.JSONDecodeError("bad json", "", 0),
        ):
            # Act
            response = client.post("/api/v1/diagnose", json=sample_diagnosis_payload)

        # Assert
        assert response.status_code == 502
        assert "parse" in response.json()["detail"].lower()

    def test_returns_500_on_unexpected_error(
        self, client: TestClient, sample_diagnosis_payload: dict
    ):
        # Arrange
        with patch(
            "app.routers.diagnosis.diagnose_vehicle",
            side_effect=RuntimeError("unexpected"),
        ):
            # Act
            response = client.post("/api/v1/diagnose", json=sample_diagnosis_payload)

        # Assert
        assert response.status_code == 500
        assert "unexpected" in response.json()["detail"].lower()


class TestChatEndpoint:
    def _make_chat_payload(self) -> dict:
        return {"message": "What tools do I need?", "history": []}

    async def _mock_stream(chunks):
        for chunk in chunks:
            yield chunk

    def test_returns_streaming_response(self, client: TestClient):
        # Arrange
        async def mock_stream(_request):
            for chunk in ["Hello", " world"]:
                yield chunk

        with patch("app.routers.chat.stream_chat", side_effect=mock_stream):
            # Act
            response = client.post("/api/v1/chat", json=self._make_chat_payload())

        # Assert
        assert response.status_code == 200
        assert "text/event-stream" in response.headers["content-type"]

    def test_response_uses_sse_format(self, client: TestClient):
        # Arrange
        async def mock_stream(_request):
            for chunk in ["Hello", " world"]:
                yield chunk

        with patch("app.routers.chat.stream_chat", side_effect=mock_stream):
            # Act
            response = client.post("/api/v1/chat", json=self._make_chat_payload())

        # Assert
        body = response.text
        assert "data: Hello" in body
        assert "data: [DONE]" in body

    def test_response_headers_prevent_caching(self, client: TestClient):
        # Arrange
        async def mock_stream(_request):
            yield "chunk"

        with patch("app.routers.chat.stream_chat", side_effect=mock_stream):
            # Act
            response = client.post("/api/v1/chat", json=self._make_chat_payload())

        # Assert
        assert response.headers.get("cache-control") == "no-cache"

    def test_returns_422_for_empty_message(self, client: TestClient):
        # Act
        response = client.post("/api/v1/chat", json={"message": "", "history": []})

        # Assert
        assert response.status_code == 422
