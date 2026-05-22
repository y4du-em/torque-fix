import os

# Must be set before any app import so pydantic-settings can resolve the key
os.environ.setdefault("ANTHROPIC_API_KEY", "sk-test-key-for-testing")

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.models.vehicle import FuelType, VehicleContext, VehicleType


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def sample_vehicle() -> dict:
    return {
        "type": "bike",
        "make": "Honda",
        "model": "CB Shine",
        "year": 2022,
        "fuel_type": "petrol",
        "engine_cc": 125,
        "mileage": 15000,
    }


@pytest.fixture
def sample_vehicle_context(sample_vehicle) -> VehicleContext:
    return VehicleContext(**sample_vehicle)


@pytest.fixture
def sample_diagnosis_payload(sample_vehicle) -> dict:
    return {
        "vehicle": sample_vehicle,
        "symptoms": ["Engine won't start or hard to start", "Rough idling"],
    }


@pytest.fixture
def sample_claude_json() -> str:
    """Raw JSON string as Claude would return it for a diagnosis."""
    return """{
        "diagnosis": "Faulty spark plug causing ignition failure.",
        "tools": [
            {"name": "Spark plug wrench", "size": "16mm", "type": "socket wrench", "required": true},
            {"name": "Feeler gauge", "size": null, "type": "gauge", "required": false}
        ],
        "parts": [
            {"name": "NGK Spark Plug", "partNumber": "CR7HSA", "quantity": 1, "estimatedCost": "₹80-₹120", "priority": "critical"}
        ],
        "steps": [
            {
                "stepNumber": 1,
                "title": "Remove spark plug",
                "description": "Unscrew the spark plug using a 16mm socket wrench.",
                "warning": "Ensure engine is cold before starting.",
                "tip": "Mark the plug wire to avoid confusion.",
                "estimatedTime": "10 minutes"
            }
        ],
        "difficulty": "easy",
        "estimatedTime": "30 minutes",
        "estimatedCost": "₹150-₹250",
        "warningFlags": ["Check fuel flow if issue persists after plug replacement."],
        "safetyNotes": ["Wear gloves and eye protection."]
    }"""
