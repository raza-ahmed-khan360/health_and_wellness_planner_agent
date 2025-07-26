from agents import Agent, GuardrailFunctionOutput, RunContextWrapper
from pydantic import BaseModel
from context import UserSessionContext
from guardrails import is_injury_related

# 🩹 Input schema
class InjurySupportInput(BaseModel):
    injury_note: str

# 🔒 Guardrail
async def injury_input_guardrail(
    ctx: RunContextWrapper[UserSessionContext],
    agent,
    input_text: str
) -> GuardrailFunctionOutput:
    is_valid = is_injury_related(input_text)
    return GuardrailFunctionOutput(
        output_info={
            "valid": is_valid,
            "reason": "Injury-related input detected." if is_valid else "No signs of injury detected."
        },
        tripwire_triggered=not is_valid
    )

# 👤 Injury Support Agent
injury_support_agent = Agent[UserSessionContext](
    name="InjurySupportAgent",
    model="gpt-4o-mini",
    instructions="Help users with workout recommendations if they have an injury."
)
