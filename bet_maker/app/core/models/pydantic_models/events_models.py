from pydantic import BaseModel, Field


class Event(BaseModel):
    name: str = Field(..., description="The name of the event")
    coefficient: float = Field(..., description="The betting coefficient for the event")
    status: int = Field(..., description="The status of the event")
