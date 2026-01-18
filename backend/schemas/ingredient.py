from pydantic import BaseModel, ConfigDict


class IngredientCategoryCreate(BaseModel):
    name: str  # bez id - baza sama nada
    
class IngredientCategoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str