from pydantic import BaseModel, Field
from typing import Dict, Optional

class TripRequest(BaseModel):
    fromLocation: str = Field(..., description="Departure location")
    destination: str = Field(..., description="Destination location")
    travelers: int = Field(..., ge=1, le=10, description="Number of travelers")
    travelDate: str = Field(..., description="Travel date (YYYY-MM)")
    duration: Optional[int] = Field(7, ge=1, le=30, description="Trip duration in days")
    interests: Dict[str, bool] = Field(..., description="Travel interests")

    class Config:
        json_schema_extra = {
            "example": {
                "fromLocation": "Bengaluru",
                "destination": "London",
                "travelers": 2,
                "travelDate": "2025-04",
                "duration": 7,
                "interests": {
                    "historical": True,
                    "nature": True,
                    "cultural": True,
                    "shopping": False,
                    "food": True,
                    "adventure": False
                }
            }
        }
