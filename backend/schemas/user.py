from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class UserBase(BaseModel):
    """Wspólne pola dla User schemas."""
    email: EmailStr
    username: str = Field(min_length=3, max_length=100)


class UserCreate(UserBase):
    """Schema do rejestracji użytkownika."""
    password: str = Field(min_length=8, max_length=100)
    date_of_birth: date
    gender: str = Field(pattern="^(male|female|other)$")
    height: float = Field(gt=0, lt=300)  # cm
    
    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain uppercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain digit")
        return v


class UserUpdate(BaseModel):
    """Schema do aktualizacji - wszystko opcjonalne."""
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=3, max_length=100)
    password: Optional[str] = Field(None, min_length=8, max_length=100)
    avatar_url: Optional[str] = None
    height: Optional[float] = Field(None, gt=0, lt=300)


class UserResponse(UserBase):
    """Schema odpowiedzi - bez hasła!"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    date_of_birth: date
    gender: str
    height: float
    avatar_url: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None


class UserLogin(BaseModel):
    """Schema do logowania."""
    email: EmailStr
    password: str