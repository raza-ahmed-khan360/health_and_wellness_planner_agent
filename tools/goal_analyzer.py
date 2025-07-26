import re
from typing import Optional
from pydantic import BaseModel
from agents import function_tool, RunContextWrapper
from context import UserSessionContext
from guardrails import goal_input, goal_output

class GoalInput(BaseModel):
    text: str

class StructuredGoal(BaseModel):
    quantity: float
    metric: str  # "kg" or "lbs"
    duration: str  # e.g. "2 months"

def parse_goal(text: str) -> Optional[StructuredGoal]:
    t = text.lower()
    pattern = r"(?:lose|gain|drop|shed|put on|reduce|cut|add)?\s*(\d+(?:\.\d+)?)\s*(?:\s)?(kg|kgs|kilograms?|pounds?|lbs?)\s*(?:in|over|within)?\s*(\d{1,2})\s*(day|days|week|weeks|month|months|year|years)"
    match = re.search(pattern, t)
    if match:
        quantity = float(match.group(1))
        metric_raw = match.group(2)
        metric = "kg" if "kg" in metric_raw else "lbs"
        duration = f"{match.group(3)} {match.group(4)}"
        return StructuredGoal(quantity=quantity, metric=metric, duration=duration)
    return None

@function_tool
async def goal_analyzer_tool(
    ctx: RunContextWrapper[UserSessionContext],
    inputs: GoalInput
) -> str:
    goal = parse_goal(inputs.text)
    if goal:
        ctx.context.goal = goal.model_dump()
        return f"🥗 Thanks for mentioning your goal. I've noted that you'd like to lose **{goal.quantity} {goal.metric}** in **{goal.duration}**. I'll generate a personalized plan to support this!"
    raise ValueError("❌ Sorry, I couldn't understand your goal. Please specify it like: 'lose 5kg in 2 months'.")
