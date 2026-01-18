from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"  # Standard OAuth2


class TokenPayload(BaseModel):
    sub: str | None = None  # subject = user_id