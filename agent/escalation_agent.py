from agents import Agent, InputGuardrail, GuardrailFunctionOutput, RunContextWrapper, function_tool
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

# 🧠 Route handler (agent logic)
async def handle_escalation(ctx: RunContextWrapper[UserSessionContext], input_text: str) -> str:
    ctx.context.handoff_logs.append(f"Escalated to human coach for: {input_text}")
    return (
        f"🚨 You mentioned: '{input_text}'. "
        "This may require help from a human coach or trainer. "
        "Please reach out to our team or expect a follow-up soon."
    )

# 👤 Escalation Agent
escalation_agent = Agent[UserSessionContext](
    name="EscalationAgent",
    model="gpt-4o-mini",
    instructions="Escalate serious user issues to a human coach."
)

@function_tool
async def handoff_escalation(ctx: RunContextWrapper[UserSessionContext], input: str) -> str:
    return await handle_escalation(ctx, input)
