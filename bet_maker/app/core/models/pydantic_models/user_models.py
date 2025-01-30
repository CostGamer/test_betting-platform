from pydantic import BaseModel, ConfigDict, Field


class UserModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: str = Field(..., description="user email")
    balance: float = Field(..., description="user current balance")
