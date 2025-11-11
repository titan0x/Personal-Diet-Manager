from typing import Dict, Any, List
from datetime import datetime, timedelta
import json


# # Class to manage ingredient information
# class IngredientService:
#     def __init__(self) -> None:
#         self.ingredients: Dict[str, Dict[str, Any]] = {}

#     def add_ingredient(self, ingredient_json: Dict[str, Any], ingredient_grams: float) -> None:
#         self.ingredients[ingredient_json["name"]] = {
#             "ingredient_macros": ingredient_json,
#             "ingredient_grams": ingredient_grams
#         }

#     def get_ingredient(self, ingredient_name: str) -> Dict[str, Any]:
#         return self.ingredients.get(ingredient_name)

#     def remove_ingredient(self, ingredient_name: str) -> None:
#         self.ingredients.pop(ingredient_name, None)

#     def clear_ingredients(self) -> None:
#         self.ingredients.clear()

        # pass ingredient as json 
        # {
        #     "name": "chicken"
        #     "serving size": "100g"
        #     "calories": "165"
        #     "total fat": "3.6g"
        #     "cholesterol": "85mg"
        #     "sodium": "74mg"
        #     "carbohydrates": "0g"
        #     "protein": "31"
        # }
        
        
        
class DietManager:
    def __init__(self, user):
        self.user = user
        if not user.diet_plan:
            self.user.diet_plan = {}

    # ---------------- Diet level ----------------
    def create_diet(self, goal: str, date_from: str, duration: int, meals_per_day: int):
        """
        date_from: string in format YYYY-MM-DD
        duration: integer (number of days)
        """
        # Convert to datetime
        start_date = datetime.strptime(date_from, "%Y-%m-%d").date()
        end_date = start_date + timedelta(days=duration)

        self.user.diet_plan = {
            "goal": goal,
            "date_from": start_date.isoformat(),  # save as ISO string
            "date_to": end_date.isoformat(),      # calculated end date
            "duration_in_days": duration,
            "meals_per_day": meals_per_day,
            "plans_per_day": []
        }
        return self.user.diet_plan
#
    def finish_diet(self):
        if self.user.diet_plan:
            if not self.user.finished_diet_plans:
                self.user.finished_diet_plans = []
            self.user.finished_diet_plans.append(self.user.diet_plan)
            self.user.diet_plan = None

    def delete_diet(self):
        self.user.diet_plan = None

    # ---------------- Day level ----------------
    def add_day_plan(self, date, calories=0, macros=None):
        if macros is None:
            macros = {"total fat": 0, "cholesterol": 0, "sodium": 0, "carbohydrates": 0, "protein": 0}

        day_plan = {
            "date": date,
            "calories": calories,
            "macros": macros,
            "meals": []
        }
        self.user.diet_plan["plans_per_day"].append(day_plan)
        return day_plan

    # ---------------- Meal level ----------------
    def add_meal(self, date, meal):
        for day in self.user.diet_plan["plans_per_day"]:
            if day["date"] == date:
                day["meals"].append(meal)
                self._recalculate_totals(day)
                return day
        raise ValueError("Day plan not found")

    def update_meal(self, date, meal_name, new_values):
        for day in self.user.diet_plan["plans_per_day"]:
            if day["date"] == date:
                for meal in day["meals"]:
                    if meal["name"] == meal_name:
                        meal.update(new_values)
                        self._recalculate_totals(day)
                        return meal
        raise ValueError("Meal not found")

    def remove_meal(self, date, meal_name):
        for day in self.user.diet_plan["plans_per_day"]:
            if day["date"] == date:
                day["meals"] = [m for m in day["meals"] if m["name"] != meal_name]
                self._recalculate_totals(day)
                return day

    # ---------------- Utility ----------------
    def _recalculate_totals(self, day):
        total_calories = 0
        total_macros = {"total fat": 0, "cholesterol": 0, "sodium": 0, "carbohydrates": 0, "protein": 0}

        for meal in day["meals"]:
            total_calories += meal.get("calories", 0)
            for k in total_macros.keys():
                total_macros[k] += meal.get("macros", {}).get(k, 0)

        day["calories"] = total_calories
        day["macros"] = total_macros
