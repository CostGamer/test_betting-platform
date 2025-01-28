from pydantic import UUID4, BaseModel, ConfigDict, Field


class RegisterUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: str = Field(..., description="user email")
    password: str = Field(..., description="user password")


class JWTUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID4 = Field(..., description="user ID")
    email: str = Field(..., description="user email")
    password: bytes = Field(..., description="user hashed password")


class JWTTokenInfo(BaseModel):
    access_token: str = Field(..., description="JWT access token")
    refresh_token: str | None = Field(default=None, description="JWT refresh token")
    token_type: str | None = Field(default="Bearer", description="token type")
