# --------------- Ingredient Service ---------------

from sqlalchemy.orm import Session
from backend.models.models import Ingredient

def create_ingredient(db: Session, ingredient_data: dict):
    ingredient = Ingredient(**ingredient_data)
    db.add(ingredient)
    db.commit()
    db.refresh(ingredient)
    return ingredient

def get_ingredient(db: Session, ingredient_id: int):
    return db.query(Ingredient).filter(Ingredient.id == ingredient_id).first()

def get_ingredients(db: Session, skip: int = 0, limit: int = 50):
    return db.query(Ingredient).offset(skip).limit(limit).all()

def update_ingredient(db: Session, ingredient_id: int, updates: dict):
    ingredient = get_ingredient(db, ingredient_id)
    if not ingredient:
        return None
    for key, value in updates.items():
        setattr(ingredient, key, value)
    db.commit()
    db.refresh(ingredient)
    return ingredient

def delete_ingredient(db: Session, ingredient_id: int):
    ingredient = get_ingredient(db, ingredient_id)
    if not ingredient:
        return None
    db.delete(ingredient)
    db.commit()
    return True

# --------------- Meal Service ---------------

