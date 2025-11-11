from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from ..databases.database import Base
from datetime import datetime, date
from typing import Optional


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))

    # Opcjonalne
    avatar_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # Podstawowe - rzadko się zmieniają
    date_of_birth: Mapped[date]
    gender: Mapped[str] = mapped_column(String(20))  # male, female, other
    height: Mapped[float]  # cm

    # Meta
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        onupdate=datetime.utcnow,
        nullable=True
    )

    # ✅ Relacje
    physical_data: Mapped[list["PhysicalData"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        order_by="PhysicalData.recorded_at.desc()"
    )

    # ✅ DODANE - relacja do planów dietetycznych
    diet_plans: Mapped[list["DietPlan"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        order_by="DietPlan.created_at.desc()"
    )

    # ✅ Properties dla wygody
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
    """Dane zmienne - tracking"""
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    weight: Mapped[float]  # kg
    activity_level: Mapped[str]  # sedentary, light, moderate, active, very_active

    # Opcjonalne pomiary
    body_fat_percentage: Mapped[Optional[float]]
    muscle_mass: Mapped[Optional[float]]
    waist_circumference: Mapped[Optional[float]]

    # Meta
    recorded_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    notes: Mapped[Optional[str]]  # Notatki użytkownika

    user: Mapped["User"] = relationship(back_populates="physical_data")