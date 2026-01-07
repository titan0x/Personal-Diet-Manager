from datetime import time, datetime
from typing import Optional, TYPE_CHECKING

from sqlalchemy import ForeignKey, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

if TYPE_CHECKING:
    from models.diet import DailyPlan
    from models.ingredient import Ingredient
    from models.user import User


class MealTemplate(Base):
    """Szablon posiłku - globalny lub użytkownika"""
    __tablename__ = "meal_templates"

    __table_args__ = (
        UniqueConstraint('name', 'user_id', name='uq_meal_template_name_user'),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150), index=True)

    # NULL = globalny, wartość = prywatny
    user_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id"),
        nullable=True
    )

    # Kategoria posiłku
    category: Mapped[str] = mapped_column(String(50))  # breakfast, lunch, dinner, snack

    # Opis (opcjonalny)
    description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # Wyliczone wartości (cache z template_ingredients)
    calories: Mapped[float] = mapped_column(default=0.0)
    protein: Mapped[float] = mapped_column(default=0.0)
    carbs: Mapped[float] = mapped_column(default=0.0)
    fats: Mapped[float] = mapped_column(default=0.0)
    fiber: Mapped[float] = mapped_column(default=0.0)

    # Meta
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    # Relacje
    user: Mapped[Optional["User"]] = relationship(back_populates="meal_templates")
    template_ingredients: Mapped[list["MealTemplateIngredient"]] = relationship(
        back_populates="template",
        cascade="all, delete-orphan"
    )

    @property
    def is_global(self) -> bool:
        """Czy szablon jest globalny (systemowy)"""
        return self.user_id is None

    def calculate_nutrition(self) -> None:
        """Przelicz wartości odżywcze z template_ingredients"""
        self.calories = sum(ti.total_calories for ti in self.template_ingredients)
        self.protein = sum(ti.total_protein for ti in self.template_ingredients)
        self.carbs = sum(ti.total_carbs for ti in self.template_ingredients)
        self.fats = sum(ti.total_fat for ti in self.template_ingredients)
        self.fiber = sum(ti.total_fiber for ti in self.template_ingredients)


class MealTemplateIngredient(Base):
    """Składnik w szablonie posiłku"""
    __tablename__ = "meal_template_ingredients"

    id: Mapped[int] = mapped_column(primary_key=True)
    template_id: Mapped[int] = mapped_column(ForeignKey("meal_templates.id"))
    ingredient_id: Mapped[int] = mapped_column(ForeignKey("ingredients.id"))

    quantity: Mapped[float]
    unit: Mapped[str] = mapped_column(String(20), default="g")

    # Relacje
    template: Mapped["MealTemplate"] = relationship(back_populates="template_ingredients")
    ingredient: Mapped["Ingredient"] = relationship()

    # Properties - identyczne jak w MealIngredient
    @property
    def quantity_in_base_units(self) -> float:
        """Przelicz na jednostkę bazową składnika"""
        if self.unit == self.ingredient.base_unit:
            return self.quantity

        for alt_unit in self.ingredient.units:
            if alt_unit.unit_name == self.unit:
                if self.ingredient.base_unit == "g":
                    return self.quantity * alt_unit.gram_equivalent

        return self.quantity

    @property
    def multiplier(self) -> float:
        """Mnożnik względem base_amount"""
        base_qty = self.quantity_in_base_units
        return base_qty / self.ingredient.base_amount

    @property
    def total_calories(self) -> float:
        return self.ingredient.calories * self.multiplier

    @property
    def total_protein(self) -> float:
        return self.ingredient.protein * self.multiplier

    @property
    def total_carbs(self) -> float:
        return self.ingredient.carbs * self.multiplier

    @property
    def total_fat(self) -> float:
        return self.ingredient.fat * self.multiplier

    @property
    def total_fiber(self) -> float:
        return self.ingredient.fiber * self.multiplier


class Meal(Base):
    __tablename__ = "meals"

    id: Mapped[int] = mapped_column(primary_key=True)
    daily_plan_id: Mapped[int] = mapped_column(ForeignKey("daily_plans.id"))

    # Opcjonalne - z jakiego szablonu skopiowano
    template_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("meal_templates.id"),
        nullable=True
    )

    # Info
    name: Mapped[str] = mapped_column(String(100))
    meal_order: Mapped[int]
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
    template: Mapped[Optional["MealTemplate"]] = relationship()
    meal_ingredients: Mapped[list["MealIngredient"]] = relationship(
        back_populates="meal",
        cascade="all, delete-orphan"
    )

    def calculate_nutrition(self) -> None:
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
    unit: Mapped[str] = mapped_column(String(20), default="g")

    # Relacje
    meal: Mapped["Meal"] = relationship(back_populates="meal_ingredients")
    ingredient: Mapped["Ingredient"] = relationship()

    # Properties
    @property
    def quantity_in_base_units(self) -> float:
        """Przelicz na jednostkę bazową składnika"""
        if self.unit == self.ingredient.base_unit:
            return self.quantity

        # Szukaj konwersji
        for alt_unit in self.ingredient.units:
            if alt_unit.unit_name == self.unit:
                if self.ingredient.base_unit == "g":
                    return self.quantity * alt_unit.gram_equivalent

        return self.quantity

    @property
    def multiplier(self) -> float:
        """Mnożnik względem base_amount"""
        base_qty = self.quantity_in_base_units
        return base_qty / self.ingredient.base_amount

    @property
    def total_calories(self) -> float:
        return self.ingredient.calories * self.multiplier

    @property
    def total_protein(self) -> float:
        return self.ingredient.protein * self.multiplier

    @property
    def total_carbs(self) -> float:
        return self.ingredient.carbs * self.multiplier

    @property
    def total_fat(self) -> float:
        return self.ingredient.fat * self.multiplier

    @property
    def total_fiber(self) -> float:
        return self.ingredient.fiber * self.multiplier