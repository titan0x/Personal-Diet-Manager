from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..databases.database import Base
from sqlalchemy import String
from sqlalchemy import ForeignKey


class Ingredient(Base):
    __tablename__ = "ingredients"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150), unique=True, index=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("ingredient_categories.id"))

    # Meta
    source_type: Mapped[str] = mapped_column(default="raw")  # raw, packaged

    # Jednostka bazowa (na ile są podane wartości)
    base_amount: Mapped[float] = mapped_column(default=100.0)
    base_unit: Mapped[str] = mapped_column(default="g")

    # ✅ Wartości odżywcze BEZPOŚREDNIO (na base_amount)
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
    units: Mapped[list["IngredientUnit"]] = relationship(back_populates="ingredient")


class IngredientCategory(Base):
    __tablename__ = "ingredient_categories"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)

    # Relacja
    ingredients: Mapped[list["Ingredient"]] = relationship(back_populates="category")


class IngredientUnit(Base):
    __tablename__ = "ingredient_units"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ingredient_id: Mapped[int] = mapped_column(ForeignKey("ingredients.id"))
    unit_name: Mapped[str] = mapped_column(String(50))  # "sztuka", "łyżka"
    gram_equivalent: Mapped[float]  # np. 120.0 (1 sztuka = 120g)

    # Relacja
    ingredient: Mapped["Ingredient"] = relationship(back_populates="units")