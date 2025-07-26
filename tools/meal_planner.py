from typing import List
from pydantic import BaseModel
from agents import function_tool, RunContextWrapper
from context import UserSessionContext, MealPlanDay
from guardrails import diet_input, mealplan_output, normalize_diet_name, is_valid_diet 

# 📥 Input model
class MealPlannerInput(BaseModel):
    diet: str

# 🛠️ Meal Planner Tool
@function_tool
async def meal_planner_tool(
    ctx: RunContextWrapper[UserSessionContext],
    inputs: MealPlannerInput
) -> str:
    normalized_diet = normalize_diet_name(inputs.diet.strip().lower())
    
    if not is_valid_diet(normalized_diet):
        ctx.context.diet_preferences = None
        ctx.context.meal_plan = []
        return "❌ Sorry, that diet is not supported."

    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    templates = {
        "vegetarian": "Protein-rich lentil and quinoa bowls with seasonal veggies.",
        "keto": "High-fat, low-carb meals with avocado, eggs, and meat.",
        "vegan": "Plant-based meals with legumes, grains, and greens.",
        "mediterranean": "Balanced meals with fish, olive oil, whole grains, and vegetables.",
        "low-carb": "Lean proteins with leafy greens and nuts.",
        "balanced": "A mix of protein, carbs, and healthy fats in each meal."
    }

    plan = [
        MealPlanDay(
            day=day,
            meal_name=f"{normalized_diet.title()} Power Bowl",
            description=templates.get(normalized_diet, "Healthy and clean meal."),
            calories=450
        ) for day in days
    ]

    ctx.context.diet_preferences = normalized_diet
    ctx.context.meal_plan = [entry.model_dump() for entry in plan]

    # Format as Markdown
    markdown = ["Here's a vegetarian meal plan for the week:\n"]
    for entry in plan:
        markdown.append(f"- **{entry.day}:** {entry.meal_name}  ")
        markdown.append(f"  _{entry.description}_ **Calories:** {entry.calories}")
    return "\n".join(markdown)
