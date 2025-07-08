from agents.tool import function_tool
from pydantic import BaseModel
from typing import Literal
from agents import RunContextWrapper
from context import UserSessionContext

# ✅ Input model for scheduling check-ins
class CheckinInput(BaseModel):
    day_of_week: Literal[
        "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
    ]
    time_of_day: str

# ✅ Output model with confirmation message
class CheckinConfirmation(BaseModel):
    message: str

# ✅ Main tool function
@function_tool("CheckinSchedulerTool")
async def checkin_scheduler_tool(
    wrapper: RunContextWrapper[UserSessionContext],
    inputs: CheckinInput
) -> CheckinConfirmation:
    # Guardrail: Validate input
    valid_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    if inputs.day_of_week not in valid_days or not inputs.time_of_day.strip():
        return CheckinConfirmation(
            message="Oops! Please give me a real day of the week and a time, like 'Monday at 9am'. Try again!"
        )

    # Initialize check-in schedule if missing
    if not wrapper.context.checkin_schedule:
        wrapper.context.checkin_schedule = []

    # Append check-in to context
    wrapper.context.checkin_schedule.append({
        "day": inputs.day_of_week,
        "time": inputs.time_of_day
    })

    return CheckinConfirmation(
        message=f"✅ Awesome! Your check-in is set for {inputs.day_of_week} at {inputs.time_of_day}."
    )
