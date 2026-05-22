import pytest

from app.models.vehicle import FuelType, TransmissionType, VehicleContext, VehicleType
from app.prompts.assistant_prompt import build_assistant_system_prompt
from app.prompts.diagnosis_prompt import build_diagnosis_system_prompt, build_diagnosis_user_prompt


@pytest.fixture
def bike_vehicle() -> VehicleContext:
    return VehicleContext(
        type=VehicleType.BIKE,
        make="Honda",
        model="CB Shine",
        year=2022,
        fuel_type=FuelType.PETROL,
        engine_cc=125,
        transmission=TransmissionType.MANUAL,
        mileage=12000,
    )


@pytest.fixture
def car_vehicle() -> VehicleContext:
    return VehicleContext(
        type=VehicleType.CAR,
        make="Hyundai",
        model="Creta",
        year=2021,
        fuel_type=FuelType.DIESEL,
        engine_cc=1497,
    )


class TestDiagnosisSystemPrompt:
    def test_returns_string(self):
        # Act
        result = build_diagnosis_system_prompt()

        # Assert
        assert isinstance(result, str)
        assert len(result) > 0

    def test_instructs_json_only_response(self):
        # Act
        result = build_diagnosis_system_prompt()

        # Assert
        assert "JSON" in result
        assert "preamble" in result or "markdown" in result

    def test_includes_all_required_schema_fields(self):
        # Act
        result = build_diagnosis_system_prompt()

        # Assert
        for field in ["diagnosis", "tools", "parts", "steps", "difficulty", "estimatedTime", "warningFlags", "safetyNotes"]:
            assert field in result

    def test_includes_difficulty_enum_values(self):
        # Act
        result = build_diagnosis_system_prompt()

        # Assert
        for level in ["easy", "medium", "hard", "professional"]:
            assert level in result


class TestDiagnosisUserPrompt:
    def test_includes_vehicle_details(self, bike_vehicle):
        # Act
        result = build_diagnosis_user_prompt(bike_vehicle, ["Engine noise"], None)

        # Assert
        assert "Honda" in result
        assert "CB Shine" in result
        assert "2022" in result
        assert "125cc" in result
        assert "petrol" in result

    def test_includes_all_symptoms(self, bike_vehicle):
        # Arrange
        symptoms = ["Engine won't start", "Rough idling", "Loss of power"]

        # Act
        result = build_diagnosis_user_prompt(bike_vehicle, symptoms, None)

        # Assert
        for symptom in symptoms:
            assert symptom in result

    def test_includes_additional_notes_when_provided(self, bike_vehicle):
        # Act
        result = build_diagnosis_user_prompt(bike_vehicle, ["Engine noise"], "Only happens when cold")

        # Assert
        assert "Only happens when cold" in result

    def test_excludes_notes_section_when_none(self, bike_vehicle):
        # Act
        result = build_diagnosis_user_prompt(bike_vehicle, ["Engine noise"], None)

        # Assert
        assert "Additional Notes" not in result

    def test_includes_mileage_when_set(self, bike_vehicle):
        # Act
        result = build_diagnosis_user_prompt(bike_vehicle, ["Noise"], None)

        # Assert
        assert "12,000 km" in result

    def test_shows_not_specified_for_missing_optional_fields(self, car_vehicle):
        # Act — car_vehicle has no transmission or mileage set
        result = build_diagnosis_user_prompt(car_vehicle, ["Noise"], None)

        # Assert
        assert "Not specified" in result


class TestAssistantSystemPrompt:
    def test_base_prompt_without_context(self):
        # Act
        result = build_assistant_system_prompt(None, None)

        # Assert
        assert "TorqueFix Assistant" in result
        assert "automotive expert" in result
        assert "Vehicle Context" not in result
        assert "Diagnosis Context" not in result

    def test_includes_vehicle_context_when_provided(self, bike_vehicle):
        # Act
        result = build_assistant_system_prompt(bike_vehicle, None)

        # Assert
        assert "Honda" in result
        assert "CB Shine" in result
        assert "2022" in result
        assert "Vehicle Context" in result

    def test_excludes_diagnosis_context_when_none(self, bike_vehicle):
        # Act
        result = build_assistant_system_prompt(bike_vehicle, None)

        # Assert
        assert "Diagnosis Context" not in result

    def test_includes_diagnosis_context_when_provided(self, bike_vehicle, sample_diagnosis_response_obj):
        # Act
        result = build_assistant_system_prompt(bike_vehicle, sample_diagnosis_response_obj)

        # Assert
        assert "Diagnosis Context" in result
        assert "easy" in result

    def test_includes_estimated_cost_in_diagnosis_context_when_present(self, bike_vehicle, sample_diagnosis_response_obj):
        # Act
        result = build_assistant_system_prompt(bike_vehicle, sample_diagnosis_response_obj)

        # Assert
        assert "₹150" in result


@pytest.fixture
def sample_diagnosis_response_obj(bike_vehicle):
    from app.models.diagnosis import DiagnosisResponse, DifficultyLevel
    return DiagnosisResponse(
        id="test-id",
        vehicle=bike_vehicle,
        symptoms=["Engine noise"],
        diagnosis="Faulty spark plug.",
        tools=[],
        parts=[],
        steps=[],
        difficulty=DifficultyLevel.EASY,
        estimated_time="30 minutes",
        estimated_cost="₹150",
        warning_flags=[],
        safety_notes=["Wear gloves."],
        created_at="2024-01-01T00:00:00Z",
    )
