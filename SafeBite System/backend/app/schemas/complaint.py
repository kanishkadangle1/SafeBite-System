from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class ComplaintCreate(BaseModel):
    description: str = Field(
        min_length=10,
        max_length=5000,
        description="The citizen's original complaint description",
    )

    business_name: Optional[str] = Field(
        default=None,
        max_length=200,
    )

    food_product: Optional[str] = Field(
        default=None,
        max_length=200,
    )

    order_channel: Optional[str] = Field(
        default=None,
        max_length=50,
    )

    platform: Optional[str] = Field(
        default=None,
        max_length=100,
    )

    order_date: Optional[date] = None

    people_affected: Optional[int] = Field(
        default=None,
        ge=1,
    )

    reported_symptoms: list[str] = Field(
        default_factory=list,
    )
