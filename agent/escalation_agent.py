from agents import Agent
from agents.tool import function_tool
from pydantic import BaseModel
from agents import RunContextWrapper
from context import UserSessionContext

class EscalationInput(BaseModel):
    issue: str

@function_tool("EscalationTool")
async def escalation_tool(
    wrapper: RunContextWrapper[UserSessionContext],
    inputs: EscalationInput
) -> str:
    wrapper.context.handoff_logs.append(f"Escalated to human coach for: {inputs.issue}")
    return (
        f"🚨 You mentioned: '{inputs.issue}'. "
        "This issue may require help from a human coach or trainer. "
        "Please reach out to our team or expect a follow-up soon."
    )

escalation_agent = Agent(
    name="EscalationAgent",
    instructions="Escalate serious issues to a human coach via the escalation tool.",
    tools=[escalation_tool],
)
