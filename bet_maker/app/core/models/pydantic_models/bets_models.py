from pydantic import UUID4, BaseModel, ConfigDict, Field


class PostBet(BaseModel):
    name: str = Field(..., description="The event name")
    money_amount: float = Field(..., description="Amount of money for specific event")


class PostBetDTO(PostBet):
    coefficient: float = Field(..., description="The betting coefficient for the event")
    result: int = Field(..., description="The result of the bet")
    user_id: UUID4 = Field(..., description="The unique identifier of the user")
    event_id: UUID4 = Field(..., description="Event ID")


class GetBet(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str = Field(..., description="The event name")
    event_id: UUID4 = Field(..., description="Event ID")
    money_amount: float = Field(..., description="Amount of money for specific event")
    coefficient: float = Field(..., description="The betting coefficient for the event")
    result: int = Field(..., description="The result of the bet")
    user_id: UUID4 = Field(..., description="The unique identifier of the user")


class ActiveBets(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str = Field(..., description="The event name")
    event_id: UUID4 = Field(..., description="Event ID")
