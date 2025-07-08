from agents.tool import function_tool
from pydantic import BaseModel
from datetime import datetime
from context import UserSessionContext
from agents import RunContextWrapper
from typing import Literal

class ProgressUpdate(BaseModel):
    category: Literal["weight", "workout", "meal", "habit"]
    value: str

class ProgressResponse(BaseModel):
    message: str

@function_tool("ProgressTrackerTool")
async def progress_tracker_tool(
    wrapper: RunContextWrapper[UserSessionContext],
    inputs: ProgressUpdate
) -> ProgressResponse:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    if not inputs.value.strip():
        return ProgressResponse(
            message="Oops! Please tell me what you did—like 'Ran 5 km'—and make sure it's not blank."
        )

    wrapper.context.progress_logs.append({
        "timestamp": now,
        "category": inputs.category,
        "value": inputs.value
    })

    return ProgressResponse(
        message=f"Great job! I saved your {inputs.category} progress for {now}: {inputs.value}"
    )
