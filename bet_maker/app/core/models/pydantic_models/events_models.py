from pydantic import BaseModel, Field


class Event(BaseModel):
    name: str = Field(..., description="The name of the event")
    event_id: str = Field(..., description="Event ID")
    coefficient: float = Field(..., description="The betting coefficient for the event")
    status: int = Field(..., description="The status of the event")
