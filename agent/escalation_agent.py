from agents import Agent, GuardrailFunctionOutput, RunContextWrapper
from pydantic import BaseModel
from context import UserSessionContext

# 🚨 Input schema
class EscalationInput(BaseModel):
    issue: str

# 🔒 Guardrail function
async def escalation_guardrail(
    ctx: RunContextWrapper[UserSessionContext],
    agent,
    input_text: str
) -> GuardrailFunctionOutput:
    is_valid = bool(input_text and input_text.strip())
    return GuardrailFunctionOutput(
        output_info={
            "valid": is_valid,
            "reason": "Issue description is valid." if is_valid else "Please describe your issue clearly."
        },
        tripwire_triggered=not is_valid
    )

# 👤 Escalation Agent
escalation_agent = Agent[UserSessionContext](
    name="EscalationAgent",
    model="gpt-4o-mini",
    instructions="Escalate serious user issues to a human coach."
)

