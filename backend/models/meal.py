from datetime import time
from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..databases.database import Base
from typing import Optional

class Meal(Base):
    __tablename__ = "meals"

    id: Mapped[int] = mapped_column(primary_key=True)
    daily_plan_id: Mapped[int] = mapped_column(ForeignKey("daily_plans.id"))

    # Info
    name: Mapped[str]  # "Śniadanie", "Lunch"
    meal_order: Mapped[int]  # 1, 2, 3, 4
    planned_time: Mapped[Optional[time]] = mapped_column(nullable=True)

    # Makro (suma z ingredients)
    calories: Mapped[float] = mapped_column(default=0.0)
    protein: Mapped[float] = mapped_column(default=0.0)
    carbs: Mapped[float] = mapped_column(default=0.0)
    fats: Mapped[float] = mapped_column(default=0.0)
    fiber: Mapped[float] = mapped_column(default=0.0)

    # Status
    is_eaten: Mapped[bool] = mapped_column(default=False)
    eaten_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)

    # Relacje
    daily_plan: Mapped["DailyPlan"] = relationship(back_populates="meals")

    # ✅ Składniki w posiłku
    meal_ingredients: Mapped[list["MealIngredient"]] = relationship(
        back_populates="meal",
        cascade="all, delete-orphan"
    )

    def calculate_nutrition(self):
        """Przelicz wartości odżywcze z ingredients"""
        self.calories = sum(mi.total_calories for mi in self.meal_ingredients)
        self.protein = sum(mi.total_protein for mi in self.meal_ingredients)
        self.carbs = sum(mi.total_carbs for mi in self.meal_ingredients)
        self.fats = sum(mi.total_fat for mi in self.meal_ingredients)
        self.fiber = sum(mi.total_fiber for mi in self.meal_ingredients)



class MealIngredient(Base):
    __tablename__ = "meal_ingredients"

    id: Mapped[int] = mapped_column(primary_key=True)
    meal_id: Mapped[int] = mapped_column(ForeignKey("meals.id"))
    ingredient_id: Mapped[int] = mapped_column(ForeignKey("ingredients.id"))

    quantity: Mapped[float]
    unit: Mapped[str] = mapped_column(default="g")

    # Relacje
    meal: Mapped["Meal"] = relationship(back_populates="meal_ingredients")
    ingredient: Mapped["Ingredient"] = relationship()

    @property
    def quantity_in_base_units(self) -> float:
        """Przelicz na jednostkę bazową składnika"""
        if self.unit == self.ingredient.base_unit:
            return self.quantity

        # Szukaj konwersji
        for alt_unit in self.ingredient.units:
            if alt_unit.unit_name == self.unit:
                # Przelicz przez gram_equivalent
                if self.ingredient.base_unit == "g":
                    return self.quantity * alt_unit.gram_equivalent

        return self.quantity

    @property
    def multiplier(self) -> float:
        base_qty = self.quantity_in_base_units
        return base_qty / self.ingredient.base_amount

    @property
    def total_calories(self) -> float:
        return self.ingredient.calories * self.multiplier

    @property
    def total_protein(self) -> float:
        return self.ingredient.nutrition.protein * self.multiplier

    @property
    def total_carbs(self) -> float:
        return self.ingredient.nutrition.carbs * self.multiplier

    @property
    def total_fat(self) -> float:
        return self.ingredient.nutrition.fat * self.multiplier

    @property
    def total_fiber(self) -> float:
        return self.ingredient.nutrition.fiber * self.multiplier