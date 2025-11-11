from pydantic import BaseModel, Field

class User(BaseModel):
    id: int
    email: str
    full_name: str | None = None
    bio: str | None = None
    age: int | None = None
    weight: float | None = None
    height: float | None = None 
    
    
class UserCreate(BaseModel):
    email: str
    password: str
    full_name: str | None = None
    bio: str | None = None
    age: int | None = None
    weight: float | None = None
    height: float | None = None
    
class UserUpdate(BaseModel):
    full_name: str | None = None
    bio: str | None = None
    age: int | None = None
    weight: float | None = None
    height: float | None = None 
    
class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str | None = None
    bio: str | None = None
    age: int | None = None
    weight: float | None = None
    height: float | None = None 
    
    class Config:
        orm_mode = True
        
        
    