from datetime import datetime, timezone
from decimal import Decimal

from pydantic import UUID4, BaseModel, Field

from .enums import EventStatus


class EventBase(BaseModel):
    name: str
    coefficient: Decimal = Field(
        ...,
        gt=1,
        decimal_places=2,
        description="Positive odds with two decimal places",
    )
    deadline: int = Field(..., description="Unix timestamp for betting deadline")


class EventCreate(EventBase):
    pass


class Event(EventBase):
    event_id: UUID4 = Field(description="Unique event identifier")
    status: EventStatus = Field(..., description="Current event status")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Event creation time",
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Last update time",
    )
