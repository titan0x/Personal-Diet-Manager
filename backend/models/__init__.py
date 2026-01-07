# Import wszystkich modeli - ważne dla Alembic i relacji
from models.user import User, PhysicalData
from models.diet import DietPlan, DailyPlan, DietGoal
from models.meal import Meal, MealIngredient, MealTemplate, MealTemplateIngredient
from models.ingredient import Ingredient, IngredientCategory, IngredientUnit

__all__ = [
    "User",
    "PhysicalData",
    "DietPlan",
    "DailyPlan",
    "DietGoal",
    "Meal",
    "MealIngredient",
    "MealTemplate",
    "MealTemplateIngredient",
    "Ingredient",
    "IngredientCategory",
    "IngredientUnit",
]