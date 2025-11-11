import pandas as pd
from backend.databases.database import get_db

from backend.models.models import Base, Ingredient, IngredientCategory, IngredientNutrition

# --- Load CIQUAL data ---
df = pd.read_csv("ciqual.csv", sep=";")  # adjust separator depending on file

# column mapping
CIQUAL_COLS = {
    "alim_code": "code",
    "alim_nom_eng": "name",
    "alim_ssgrp_nom_eng": "category",
    "Energy, N x Jones' factor, with fibres (kcal/100g)": "calories",
    "Protein (g/100g)": "protein",
    "Fat (g/100g)": "fat",
    "Carbohydrate (g/100g)": "carbs",
    "Fibres (g/100g)": "fiber",
    "Sugars (g/100g)": "sugar",
    "Sodium (mg/100g)": "sodium",
    "Cholesterol (mg/100g)": "cholesterol"
}

df = df.rename(columns=CIQUAL_COLS)

session = next(get_db())

# --- Category cache ---
categories = {}

for _, row in df.iterrows():
    # Handle category
    cat_name = row["category"]
    if cat_name not in categories:
        cat = IngredientCategory(name=cat_name)
        session.add(cat)
        session.flush()  # get id
        categories[cat_name] = cat
    else:
        cat = categories[cat_name]

    # Create ingredient
    ingredient = Ingredient(
        id=int(row["code"]),  # use CIQUAL code as primary key
        name=row["name"],
        category=cat,
        unit="g",
        source_type="raw"
    )
    session.add(ingredient)
    session.flush()

    # Create nutrition
    nutrition = IngredientNutrition(
        ingredient=ingredient,
        per_amount=100,
        per_unit="g",
        calories=row.get("calories", 0) or 0,
        protein=row.get("protein", 0) or 0,
        fat=row.get("fat", 0) or 0,
        carbs=row.get("carbs", 0) or 0,
        fiber=row.get("fiber", 0) or 0,
        sugar=row.get("sugar", 0) or 0
    )
    session.add(nutrition)

session.commit()
print("✅ Imported CIQUAL data into database")
