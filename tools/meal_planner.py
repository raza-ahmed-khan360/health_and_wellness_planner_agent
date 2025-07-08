from pydantic import BaseModel
from typing import List
from agents.tool import function_tool
from agents import RunContextWrapper
from context import UserSessionContext, MealPlanDay
from guardrails import normalize_diet_name, is_valid_diet


# 📥 Input schema
class MealPlannerInput(BaseModel):
    diet: str

# 🍽️ Tool implementation
@function_tool("MealPlannerTool")
async def meal_planner_tool(
    wrapper: RunContextWrapper[UserSessionContext],
    inputs: MealPlannerInput
) -> List[MealPlanDay]:
    raw_diet = inputs.diet.strip().lower()
    normalized_diet = normalize_diet_name(raw_diet)

    # If diet is not valid, clear context and return empty meal plan
    if not is_valid_diet(normalized_diet):
        wrapper.context.diet_preferences = None
        wrapper.context.meal_plan = None
        return []

    # Generate a 7-day meal plan
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    description_templates = {
        "vegetarian": "Plant-based with lentils, chickpeas, and grains.",
        "vegan": "100% plant-based with no animal products.",
        "keto": "Low-carb, high-fat meals with healthy oils and proteins.",
        "paleo": "Whole foods, lean proteins, nuts, and no grains or dairy.",
        "diabetic": "Low-glycemic meals with stable blood sugar focus.",
        "gluten-free": "Balanced, gluten-free meals with rice, corn, and vegetables."
    }

    meal_plan = [
        MealPlanDay(
            day=day,
            meal_name=f"{normalized_diet.title()} Power Bowl",
            description=description_templates.get(normalized_diet, "Healthy and nutritious."),
            calories=450
        )
        for day in days
    ]

    # Save to context
    wrapper.context.diet_preferences = normalized_diet
    wrapper.context.meal_plan = [day.model_dump() for day in meal_plan]

    return meal_plan
