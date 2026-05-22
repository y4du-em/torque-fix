import pytest
from pydantic import ValidationError

from app.models.chat import ChatMessage, ChatRequest, MessageRole
from app.models.diagnosis import DiagnosisRequest, DiagnosisResponse, Part, PartPriority, RepairStep, Tool
from app.models.vehicle import FuelType, TransmissionType, VehicleContext, VehicleType


class TestVehicleContext:
    def test_valid_minimal(self):
        # Arrange
        data = {"type": "bike", "make": "Honda", "model": "CB Shine", "year": 2022, "fuel_type": "petrol"}

        # Act
        vehicle = VehicleContext(**data)

        # Assert
        assert vehicle.make == "Honda"
        assert vehicle.year == 2022
        assert vehicle.engine_cc is None
        assert vehicle.mileage is None

    def test_valid_full(self):
        # Arrange
        data = {
            "type": "car",
            "make": "Maruti",
            "model": "Swift",
            "year": 2020,
            "fuel_type": "petrol",
            "engine_cc": 1197,
            "transmission": "manual",
            "mileage": 45000,
        }

        # Act
        vehicle = VehicleContext(**data)

        # Assert
        assert vehicle.engine_cc == 1197
        assert vehicle.transmission == TransmissionType.MANUAL
        assert vehicle.mileage == 45000

    def test_year_below_minimum_rejected(self):
        # Arrange
        data = {"type": "bike", "make": "Honda", "model": "CB", "year": 1989, "fuel_type": "petrol"}

        # Act / Assert
        with pytest.raises(ValidationError) as exc_info:
            VehicleContext(**data)
        assert "year" in str(exc_info.value)

    def test_year_above_maximum_rejected(self):
        # Arrange
        data = {"type": "bike", "make": "Honda", "model": "CB", "year": 2026, "fuel_type": "petrol"}

        # Act / Assert
        with pytest.raises(ValidationError):
            VehicleContext(**data)

    def test_engine_cc_below_minimum_rejected(self):
        # Arrange
        data = {"type": "bike", "make": "Honda", "model": "CB", "year": 2022, "fuel_type": "petrol", "engine_cc": 10}

        # Act / Assert
        with pytest.raises(ValidationError):
            VehicleContext(**data)

    def test_engine_cc_above_maximum_rejected(self):
        # Arrange
        data = {"type": "bike", "make": "Honda", "model": "CB", "year": 2022, "fuel_type": "petrol", "engine_cc": 99999}

        # Act / Assert
        with pytest.raises(ValidationError):
            VehicleContext(**data)

    def test_negative_mileage_rejected(self):
        # Arrange
        data = {"type": "bike", "make": "Honda", "model": "CB", "year": 2022, "fuel_type": "petrol", "mileage": -1}

        # Act / Assert
        with pytest.raises(ValidationError):
            VehicleContext(**data)

    def test_invalid_fuel_type_rejected(self):
        # Arrange
        data = {"type": "bike", "make": "Honda", "model": "CB", "year": 2022, "fuel_type": "kerosene"}

        # Act / Assert
        with pytest.raises(ValidationError):
            VehicleContext(**data)

    def test_invalid_vehicle_type_rejected(self):
        # Arrange
        data = {"type": "helicopter", "make": "Honda", "model": "CB", "year": 2022, "fuel_type": "petrol"}

        # Act / Assert
        with pytest.raises(ValidationError):
            VehicleContext(**data)


class TestDiagnosisRequest:
    def test_empty_symptoms_rejected(self, sample_vehicle):
        # Arrange
        data = {"vehicle": sample_vehicle, "symptoms": []}

        # Act / Assert
        with pytest.raises(ValidationError):
            DiagnosisRequest(**data)

    def test_too_many_symptoms_rejected(self, sample_vehicle):
        # Arrange
        data = {"vehicle": sample_vehicle, "symptoms": [f"symptom {i}" for i in range(21)]}

        # Act / Assert
        with pytest.raises(ValidationError):
            DiagnosisRequest(**data)

    def test_additional_notes_too_long_rejected(self, sample_vehicle):
        # Arrange
        data = {"vehicle": sample_vehicle, "symptoms": ["Engine noise"], "additional_notes": "x" * 1001}

        # Act / Assert
        with pytest.raises(ValidationError):
            DiagnosisRequest(**data)

    def test_valid_request_with_notes(self, sample_vehicle):
        # Arrange
        data = {"vehicle": sample_vehicle, "symptoms": ["Engine noise"], "additional_notes": "Only at idle"}

        # Act
        req = DiagnosisRequest(**data)

        # Assert
        assert req.additional_notes == "Only at idle"
        assert len(req.symptoms) == 1


class TestChatRequest:
    def test_empty_message_rejected(self):
        # Act / Assert
        with pytest.raises(ValidationError):
            ChatRequest(message="")

    def test_message_too_long_rejected(self):
        # Act / Assert
        with pytest.raises(ValidationError):
            ChatRequest(message="x" * 2001)

    def test_history_too_long_rejected(self):
        # Arrange
        messages = [
            ChatMessage(id=str(i), role=MessageRole.USER, content="hi", created_at="2024-01-01T00:00:00Z")
            for i in range(51)
        ]

        # Act / Assert
        with pytest.raises(ValidationError):
            ChatRequest(message="hello", history=messages)

    def test_valid_chat_request(self):
        # Act
        req = ChatRequest(message="What tools do I need?")

        # Assert
        assert req.message == "What tools do I need?"
        assert req.history == []
        assert req.vehicle_context is None
