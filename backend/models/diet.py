from datetime import date, datetime
from typing import Optional, TYPE_CHECKING

from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from database import Base

if TYPE_CHECKING:
    from models.user import User
    from models.meal import Meal

class DietGoal(str, enum.Enum):
    WEIGHT_LOSS = "weight_loss"
    MUSCLE_GAIN = "muscle_gain"
    MAINTENANCE = "maintenance"
    HEALTH = "health"

class DietPlan(Base):
    __tablename__ = "diet_plans"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    # Podstawowe info
    name: Mapped[str] = mapped_column(String(200)) # np. "Redukcja masa - styczeń 2025"
    goal: Mapped[DietGoal] # weight_loss, muscle_gain, maintenance, health

    # Daty
    date_from: Mapped[date]
    date_to: Mapped[date]

    # Konfiguracja
    meals_per_day: Mapped[int]  # 3, 4, 5
    target_calories: Mapped[int]  # Docelowe dzienne kalorie

    # Status
    is_active: Mapped[bool] = mapped_column(default=True)
    is_completed: Mapped[bool] = mapped_column(default=False)

    # Meta
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    # Relacje
    user: Mapped["User"] = relationship(back_populates="diet_plans")
    
    daily_plans: Mapped[list["DailyPlan"]] = relationship(
        back_populates="diet_plan",
        cascade="all, delete-orphan",
        order_by="DailyPlan.date"
    )
    


    @property
    def duration_in_days(self) -> int:
        """Wylicz długość planu"""
        return (self.date_to - self.date_from).days + 1 

    @property
    def progress_percentage(self) -> float:
        """Procent ukończenia"""
        total_days = self.duration_in_days
        completed_days = len([d for d in self.daily_plans if d.is_completed])
        return (completed_days / total_days * 100) if total_days > 0 else 0



class DailyPlan(Base):
    __tablename__ = "daily_plans"

    id: Mapped[int] = mapped_column(primary_key=True)
    diet_plan_id: Mapped[int] = mapped_column(ForeignKey("diet_plans.id"))
    date: Mapped[date]

    # Cele makro na ten dzień (może się różnić od target_calories w planie)
    target_calories: Mapped[int]
    target_protein: Mapped[float]  
    target_carbs: Mapped[float]
    target_fats: Mapped[float]

    # Rzeczywiste wartości (sum z meals)
    actual_calories: Mapped[int] = mapped_column(default=0)
    actual_protein: Mapped[float] = mapped_column(default=0.0)
    actual_carbs: Mapped[float] = mapped_column(default=0.0)
    actual_fats: Mapped[float] = mapped_column(default=0.0)

    # Opcjonalne mikro
    actual_fiber: Mapped[Optional[float]] = mapped_column(nullable=True)
    actual_sodium: Mapped[Optional[float]] = mapped_column(nullable=True)
    actual_cholesterol: Mapped[Optional[float]] = mapped_column(nullable=True)

    # Status
    is_completed: Mapped[bool] = mapped_column(default=False)
    completed_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)

    # Notatki
    notes: Mapped[Optional[str]] = mapped_column(nullable=True)

    # Relacje
    diet_plan: Mapped["DietPlan"] = relationship(back_populates="daily_plans")


    meals: Mapped[list["Meal"]] = relationship(
        back_populates="daily_plan",
        cascade="all, delete-orphan",
        order_by="Meal.meal_order"
    )

    @property
    def calories_percentage(self) -> float:
        """Procent zrealizowanych kalorii"""
        return (self.actual_calories / self.target_calories * 100) if self.target_calories > 0 else 0

    def calculate_totals(self) -> None:
        """Przelicz sumę z meals"""
        self.actual_calories = int(sum(m.calories for m in self.meals))
        self.actual_protein = sum(m.protein for m in self.meals)
        self.actual_carbs = sum(m.carbs for m in self.meals)
        self.actual_fats = sum(m.fats for m in self.meals)