from enum import Enum

from pydantic import BaseModel, Field


class FuelType(str, Enum):
    PETROL = "petrol"
    DIESEL = "diesel"
    ELECTRIC = "electric"
    HYBRID = "hybrid"


class VehicleType(str, Enum):
    BIKE = "bike"
    CAR = "car"
    TRUCK = "truck"
    SCOOTER = "scooter"


class TransmissionType(str, Enum):
    MANUAL = "manual"
    AUTOMATIC = "automatic"


class VehicleContext(BaseModel):
    type: VehicleType
    make: str
    model: str
    year: int = Field(ge=1990, le=2025)
    engine_cc: int | None = Field(default=None, ge=50, le=10000)
    fuel_type: FuelType
    transmission: TransmissionType | None = None
    mileage: int | None = Field(default=None, ge=0)
