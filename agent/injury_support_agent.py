from agents import Agent, RunContextWrapper
from agents.tool import function_tool
from pydantic import BaseModel
from context import UserSessionContext

# 🩹 Input schema for the tool
class InjurySupportInput(BaseModel):
    injury_note: str

# 🛠️ Tool definition
@function_tool("InjurySupportTool")
async def injury_support_tool(
    wrapper: RunContextWrapper[UserSessionContext],
    inputs: InjurySupportInput
) -> str:
    # ✅ Use wrapper.context to access user context (as per OpenAI SDK)
    wrapper.context.injury_notes = inputs.injury_note
    wrapper.context.handoff_logs.append("Handoff to InjurySupportAgent")

    return (
        f"🩹 Based on your input: '{inputs.injury_note}', I recommend gentle, low-impact exercises "
        "like yoga, stretching, or light walking. Always consult a medical professional before continuing workouts."
    )

# 🧠 Agent definition
injury_support_agent = Agent(
    name="InjurySupportAgent",
    instructions="Assist users with injury-safe workouts using the injury support tool.",
    tools=[injury_support_tool],
)
