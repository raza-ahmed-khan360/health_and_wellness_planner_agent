from pydantic import BaseModel
from typing import Literal, Union, List
from agents import Agent, RunContextWrapper, input_guardrail, GuardrailFunctionOutput, function_tool
from context import UserSessionContext

# 📥 Input schema
class CheckinInput(BaseModel):
    day_of_week: Literal[
        "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
    ]
    time_of_day: str  # e.g., "9am" or "14:00"

# 📤 Output schema
class CheckinConfirmation(BaseModel):
    message: str

# 🔒 Input guardrail to validate format
@input_guardrail
async def checkin_input_guardrail(
    ctx: RunContextWrapper[UserSessionContext],
    agent: Agent,
    input: Union[str, List[dict]]
) -> GuardrailFunctionOutput:
    try:
        # Flatten input if it's a list of messages
        if isinstance(input, list):
            input_text = " ".join(msg.get("content", "") for msg in input if msg.get("role") == "user")
        else:
            input_text = input

        # Access the day_of_week enum or list of valid days
        valid_days = CheckinInput.__annotations__['day_of_week'] if isinstance(CheckinInput.__annotations__['day_of_week'], list) else []
        
        # Check for day and time indicators
        if any(day.lower() in input_text.lower() for day in valid_days):
            if ":" in input_text or "am" in input_text.lower() or "pm" in input_text.lower():
                return GuardrailFunctionOutput(
                    output_info={"valid": True, "reason": "Valid check-in request."},
                    tripwire_triggered=False
                )

        return GuardrailFunctionOutput(
            output_info={"valid": False, "reason": "Please specify a valid day and time (e.g., Friday at 10am)."},
            tripwire_triggered=True
        )

    except Exception as e:
        return GuardrailFunctionOutput(
            output_info={"valid": False, "reason": f"Error validating input: {str(e)}"},
            tripwire_triggered=True
        )

# ✅ Final tool definition
@function_tool
async def checkin_scheduler_tool(
    wrapper: RunContextWrapper[UserSessionContext],
    inputs: CheckinInput
) -> str:
    wrapper.context.checkin_schedule.append({
        "day": inputs.day_of_week,
        "time": inputs.time_of_day
    })
    return f"✅ Check-in scheduled for **{inputs.day_of_week}** at **{inputs.time_of_day}**!"
