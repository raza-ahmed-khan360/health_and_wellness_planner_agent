from pydantic import BaseModel
from typing import Literal, Optional
from agents import function_tool, RunContextWrapper
from context import UserSessionContext

# 📥 Input schema
class ProgressInput(BaseModel):
    date: str  # e.g., "2024-07-26"
    weight: float  # e.g., 70.5
    metric: Literal["kg", "lbs"]

# 📤 Output schema
class ProgressLog(BaseModel):
    message: str

# 🛠️ Final tool definition
@function_tool
async def progress_tracker_tool(
    wrapper: RunContextWrapper[UserSessionContext],
    inputs: ProgressInput
) -> str:
    log = {
        "date": inputs.date,
        "weight": inputs.weight,
        "metric": inputs.metric
    }
    wrapper.context.progress_logs.append(log)
    return f"✅ Logged your weight update for **{inputs.date}**: **{inputs.weight}{inputs.metric}**"
