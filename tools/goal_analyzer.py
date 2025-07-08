import re
from agents.tool import function_tool
from pydantic import BaseModel
from typing import Literal, Optional
from context import UserSessionContext
from agents import RunContextWrapper

# 📥 Define input/output models
class GoalInput(BaseModel):
    text: str

class StructuredGoal(BaseModel):
    quantity: float
    metric: Literal["kg", "lbs"]
    duration: str

def parse_goal(text: str) -> Optional[StructuredGoal]:
    text = text.lower()
    quantity_match = re.search(r"(\d+(\.\d+)?)", text)
    metric_match = re.search(r"\b(kg|kgs|kilograms|pounds|lbs)\b", text)
    duration_match = re.search(r"\b(in\s*)?(\d+)\s?(week|month|year|day)s?\b", text)
    if quantity_match and metric_match and duration_match:
        quantity = float(quantity_match.group(1))
        raw_metric = metric_match.group(1).lower()
        metric = "kg" if "kg" in raw_metric else "lbs"
        duration = duration_match.group(0).replace("in", "").strip()
        return StructuredGoal(quantity=quantity, metric=metric, duration=duration)
    return None

@function_tool("GoalAnalyzerTool")
async def goal_analyzer_tool(
    wrapper: RunContextWrapper[UserSessionContext],
    inputs: GoalInput
) -> Optional[StructuredGoal]:
    """
    Parses user goal text into structured form and saves it to context.
    """
    goal = parse_goal(inputs.text)
    if goal:
        wrapper.context.goal = goal.model_dump()
        return goal
    return None
