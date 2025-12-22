from typing import Optional

from sqlalchemy import String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Ingredient(Base):
    __tablename__ = "ingredients"
    
    # Constraint - unikalna para (name, user_id)
    __table_args__ = (
        UniqueConstraint('name', 'user_id', name='uq_ingredient_name_user'),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150), index=True)  # bez unique!
    category_id: Mapped[int] = mapped_column(ForeignKey("ingredient_categories.id"))
    
    # Właściciel - NULL = globalny
    user_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id"),
        nullable=True
    )

    source_type: Mapped[str] = mapped_column(String(20), default="raw")
    base_amount: Mapped[float] = mapped_column(default=100.0)
    base_unit: Mapped[str] = mapped_column(String(20), default="g")

    # Wartości odżywcze
    calories: Mapped[float] = mapped_column(default=0.0)
    protein: Mapped[float] = mapped_column(default=0.0)
    fat: Mapped[float] = mapped_column(default=0.0)
    carbs: Mapped[float] = mapped_column(default=0.0)
    fiber: Mapped[float] = mapped_column(default=0.0)
    sugar: Mapped[float] = mapped_column(default=0.0)
    sodium: Mapped[float] = mapped_column(default=0.0)
    cholesterol: Mapped[float] = mapped_column(default=0.0)

    # Relacje
    category: Mapped["IngredientCategory"] = relationship(back_populates="ingredients")
    user: Mapped[Optional["User"]] = relationship(back_populates="custom_ingredients")
    units: Mapped[list["IngredientUnit"]] = relationship(back_populates="ingredient")

    @property
    def is_global(self) -> bool:
        return self.user_id is None


class IngredientCategory(Base):
    __tablename__ = "ingredient_categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)

    ingredients: Mapped[list["Ingredient"]] = relationship(back_populates="category")


class IngredientUnit(Base):
    __tablename__ = "ingredient_units"

    id: Mapped[int] = mapped_column(primary_key=True)
    ingredient_id: Mapped[int] = mapped_column(ForeignKey("ingredients.id"))
    unit_name: Mapped[str] = mapped_column(String(50))
    gram_equivalent: Mapped[float]

    ingredient: Mapped["Ingredient"] = relationship(back_populates="units")