from datetime import datetime, date
from typing import Optional, TYPE_CHECKING

from sqlalchemy import String, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

if TYPE_CHECKING:
    from models.diet import DietPlan
    from models.ingredient import Ingredient
    from models.meal import MealTemplate


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))

    # Opcjonalne
    avatar_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # Podstawowe dane
    date_of_birth: Mapped[date]
    gender: Mapped[str] = mapped_column(String(20))
    height: Mapped[float]

    # Meta
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        onupdate=func.now(),
        nullable=True
    )

    # Relacje
    physical_data: Mapped[list["PhysicalData"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        order_by="PhysicalData.recorded_at.desc()"
    )

    diet_plans: Mapped[list["DietPlan"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        order_by="DietPlan.created_at.desc()"
    )

    custom_ingredients: Mapped[list["Ingredient"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )

    meal_templates: Mapped[list["MealTemplate"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )

    # Properties
    @property
    def age(self) -> int:
        """Wylicz wiek na podstawie daty urodzenia"""
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )

    @property
    def current_physical_data(self) -> Optional["PhysicalData"]:
        """Pobierz najnowsze dane fizyczne"""
        return self.physical_data[0] if self.physical_data else None

    @property
    def active_diet_plan(self) -> Optional["DietPlan"]:
        """Pobierz aktywny plan dietetyczny"""
        return next(
            (plan for plan in self.diet_plans if plan.is_active),
            None
        )


class PhysicalData(Base):
    __tablename__ = "physical_data"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    weight: Mapped[float]
    activity_level: Mapped[str] = mapped_column(String(50))

    # Opcjonalne pomiary
    body_fat_percentage: Mapped[Optional[float]] = mapped_column(nullable=True)
    muscle_mass: Mapped[Optional[float]] = mapped_column(nullable=True)
    waist_circumference: Mapped[Optional[float]] = mapped_column(nullable=True)

    # Meta
    recorded_at: Mapped[datetime] = mapped_column(server_default=func.now())
    notes: Mapped[Optional[str]] = mapped_column(nullable=True)

    # Relacje
    user: Mapped["User"] = relationship(back_populates="physical_data")