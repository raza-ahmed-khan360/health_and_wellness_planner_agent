from agents import Agent, InputGuardrail, GuardrailFunctionOutput, RunContextWrapper, function_tool
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

# 🧠 Route handler
async def handle_injury_support(ctx: RunContextWrapper[UserSessionContext], input_text: str) -> str:
    ctx.context.injury_notes = input_text
    ctx.context.handoff_logs.append("Handoff to InjurySupportAgent")
    return (
        f"🩹 Based on your note: '{input_text}', I recommend gentle, low-impact exercises "
        "like yoga, stretching, or light walking. Always consult a medical professional before continuing workouts."
    )

# 👤 Injury Support Agent
injury_support_agent = Agent[UserSessionContext](
    name="InjurySupportAgent",
    model="gpt-4o-mini",
    instructions="Help users with workout recommendations if they have an injury."
)

@function_tool
async def handoff_injury_support(ctx: RunContextWrapper[UserSessionContext], input: str) -> str:
    return await handle_injury_support(ctx, input)
