class Macronutrients:
    def __init__(self, sex:str, weight:int, height:int, age:int, activity_level = None) -> None:
        self.sex = ""
        self.weight:int = 0
        self.height:int = 0
        self.age:int = 0
        self.activity_level = None 
        bmr:int = 0  
    def calculate_bmr(self):
        """
        Calculate BMR using the Mifflin-St Jeor equation.

        Parameters:
        weight (float): Weight in kilograms
        height (float): Height in centimeters
        age (int): Age in years
        sex (str): 'male' or 'female'
        activity_level (str, optional): Choose from ['sedentary', 'light', 'moderate', 'very', 'super']

        Returns:
        float: BMR or TDEE (if activity_level provided)
        """
        if self.sex.lower() == "male" or self.sex.lower() == "m":
            bmr = 10 * self.weight + 6.25 * self.height - 5 * self.age + 5
        elif self.sex.lower() =="female" or self.sex.lower() =="f":
            bmr = 10 * self.weight + 6.25 * self.height - 5 * self.age - 161
        else:
            raise ValueError("Sex must be 'male' or 'female'.")

        activity_multipliers = {
        'sedentary': 1.2,
        'light': 1.375,
        'moderate': 1.55,
        'very': 1.725,
        'super': 1.9
    }
        if self.activity_level:
            activity_level = self.activity_level.lower()
            if activity_level in activity_multipliers:
                return round(bmr * activity_multipliers[activity_level],2)
            else:
                raise ValueError("Invalid activity level. Choose from: sedentary, light, moderate, very, super.")
        
        return round(bmr, 2)

    def calculate_macros(self, goal:str):
        """
        Calculate macronutrient distribution based on goal.

        Parameters:
        bmr (float): Basal Metabolic Rate
        goal (str): 'maintain', 'lose', or 'gain'

        Returns:
        dict: Macronutrient distribution in grams
        """
        if goal.lower() == "maintain":
            calories = self.calculate_bmr()
            protein = self.weight * 2.2 # 2.2g per kg of body weight        
            fat = (0.25 * calories) / 9 # 25% of calories from fat
            carbs = (calories - (protein * 4 + fat * 9)) / 4 # Remaining calories from carbs
        elif goal.lower() == "lose":
            calories = self.calculate_bmr() - 500   # 500 calorie deficit for weight loss               
            protein = self.weight * 2.5 # 2.5g per kg of body weight        
            fat = (0.30 * calories) / 9 # 30% of calories from fat
            carbs = (calories - (protein * 4 + fat * 9)) / 4 # Remaining calories from carbs
        elif goal.lower() == "gain":                
            calories = self.calculate_bmr() + 500                   # 500 calorie surplus for weight gain
            protein = self.weight * 2.0 # 2.0g per kg of    body weight             
            fat = (0.20 * calories) / 9 # 20% of calories from fat
            carbs = (calories - (protein * 4 + fat * 9)) / 4 # Remaining calories from carbs
        else:
            raise ValueError("Goal must be 'maintain', 'lose', or 'gain'.")     
        return {
            "calories": round(calories, 2),
            "protein_g": round(protein, 2),
            "fat_g": round(fat, 2),
            "carbs_g": round(carbs, 2)
        }       
        
    def adjust_macros_for_diet(self, diet_type:str, macros:dict):
        """
        Adjust macronutrient distribution based on diet type.

        Parameters:
        diet_type (str): 'keto', 'paleo', 'vegan', or 'vegetarian'
        macros (dict): Original macronutrient distribution

        Returns:
        dict: Adjusted macronutrient distribution
        """
        diet_type = diet_type.lower()
        if diet_type == "keto":
            # Keto: 70% fat, 20% protein, 10% carbs
            total_calories = macros['calories']
            fat = (0.70 * total_calories) / 9
            protein = (0.20 * total_calories) / 4
            carbs = (0.10 * total_calories) / 4
        elif diet_type == "paleo":
            # Paleo: 35% protein, 35% fat, 30% carbs
            total_calories = macros['calories']
            protein = (0.35 * total_calories) / 4
            fat = (0.35 * total_calories) / 9
            carbs = (0.30 * total_calories) / 4
        elif diet_type == "vegan":
            # Vegan: 20% protein, 30% fat, 50% carbs
            total_calories = macros['calories']
            protein = (0.20 * total_calories) / 4
            fat = (0.30 * total_calories) / 9
            carbs = (0.50 * total_calories) / 4
        elif diet_type == "vegetarian":
            # Vegetarian: 25% protein, 30% fat, 45% carbs
            total_calories = macros['calories']
            protein = (0.25 * total_calories) / 4
            fat = (0.30 * total_calories) / 9
            carbs = (0.45 * total_calories) / 4
        else:
            raise ValueError("Diet type must be 'keto', 'paleo', 'vegan', or 'vegetarian'.")
        
        return {
            "calories": round(total_calories, 2),
            "protein_g": round(protein, 2),
            "fat_g": round(fat, 2),
            "carbs_g": round(carbs, 2)      
        }       
        
        
    def macro_distribution_per_meal(self, macros:dict, meals_per_day:int):
        """
        Distribute macronutrients evenly across meals.

        Parameters:
        macros (dict): Macronutrient distribution
        meals_per_day (int): Number of meals per day

        Returns:
        dict: Macronutrient distribution per meal
        """
        if meals_per_day <= 0:
            raise ValueError("Meals per day must be a positive integer.")
        
        return {
            "calories_per_meal": round(macros['calories'] / meals_per_day, 2),
            "protein_g_per_meal": round(macros['protein_g'] / meals_per_day, 2),
            "fat_g_per_meal": round(macros['fat_g'] / meals_per_day, 2),
            "carbs_g_per_meal": round(macros['carbs_g'] / meals_per_day, 2)
        }
