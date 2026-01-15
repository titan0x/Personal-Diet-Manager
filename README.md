# Personal Diet Manager

# Application Overview ****

The application is a **personalized nutrition and diet planning system** that calculates individual macronutrient needs, automatically adjusts recipes to match those needs, and builds daily meal plans using an intelligent dish-selection mechanism.

The core idea is to treat **macronutrients as a constraint system**, while dishes and recipes dynamically adapt to the user’s goals.

# Core Modules & Features

## 1. Macronutrients Calculator

This module is responsible for calculating the user’s daily energy and macronutrient requirements.

### Data Collection

The application collects the following user inputs:

- Age
- Gender
- Height
- Current weight
- Activity level
- Goal weight
- (Optional) Body fat percentage

### Calculation Models

The user can choose between two scientifically recognized models:

- **Mifflin–St Jeor equation**
- **Katch–McArdle equation** (used when body fat data is available)

### Output

- Basal Metabolic Rate (BMR)
- Total Daily Energy Expenditure (TDEE)
- Daily macronutrient targets:
    - Proteins
    - Fats
    - Carbohydrates

These values form the **base macronutrient profile**, stored in memory and used across the entire application.

## 2. Personal Cooking Book (Recipe Engine)

This module acts as a **dynamic recipe database**, personalized for the user.

### Dish Model

Each dish is treated as a **class** with properties such as:

- Ingredients
- Base ingredient quantities
- Macronutrient values per ingredient
- Dish category (e.g. breakfast, lunch, dinner, snack)
- Base macros (P/F/C/kcal)

### Dynamic Scaling

- Ingredient volumes are **automatically scaled** to match the user’s macronutrient targets.
- When macronutrients change (e.g. new goal weight), all dishes are recalculated proportionally.
- One dish definition can adapt to many different users.

This allows the cookbook to remain reusable while staying fully personalized.

## 3. Diet Planner (Meal Planning Engine)

This is the core logic module that builds daily meal plans.

### Daily Planning Logic

- The user defines the number of daily meals (e.g. 3, 4, 5).
- Daily macronutrients are **divided across meals** using a dedicated method.
- Each meal receives a target macro allocation.

### Dish Selection

- Dishes are drawn from the personal cooking book based on:
    - Meal category
    - Proximity to target macros
- The system selects dishes whose macronutrient profile is closest to the remaining macro budget.

### Macro Balancing

- After selecting a dish:
    - Dish macros are subtracted from the remaining daily macros.
    - Remaining meals are recalculated dynamically.
- This prevents macro overflow and improves daily balance.

## 4. Key Methods & Internal Logic

The diet planner exposes several core methods:

### Macronutrient Distribution Method

- Divides daily macronutrients into meal-level targets.
- Supports different strategies (equal split, protein-priority, custom ratios).

### Dish Drawing Method

- Selects appropriate dishes from the cookbook.
- Matches meal category and macro proximity.
- Adds selected dishes to daily meals.

### Dish Editing Method

- Allows manual modification of a dish:
    - Ingredients
    - Quantities
    - Macros
- Triggers recalculation of dependent values.

### Recalculation Method

- When user macros change:
    - All dish ingredient volumes are recalculated.
    - All daily meal plans are updated accordingly.
- Ensures consistency across the entire system.

# Overall Architecture Concept

- **User profile** defines macronutrient constraints
- **Cooking book** provides flexible building blocks
- **Diet planner** acts as an optimization layer
- **Dishes** behave as dynamic objects rather than static recipes

The application combines **nutrition science, object-oriented design, and constraint-based planning** to create a fully personalized diet system.
