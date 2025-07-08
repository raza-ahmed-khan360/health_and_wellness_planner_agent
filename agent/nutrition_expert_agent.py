from agents import Agent
from agents.tool import function_tool
from pydantic import BaseModel
from agents import RunContextWrapper
from context import UserSessionContext

class NutritionInput(BaseModel):
    condition: str

@function_tool("NutritionExpertTool")
async def nutrition_expert_tool(
    wrapper: RunContextWrapper[UserSessionContext],
    inputs: NutritionInput
) -> str:
    wrapper.context.handoff_logs.append(f"NutritionExpertAgent consulted for: {inputs.condition}")
    return (
        f"🥗 Thanks for mentioning your condition: '{inputs.condition}'. "
        "Based on that, I'll ensure all meal plans follow dietary restrictions. "
        "Avoid processed sugars, maintain hydration, and stick to whole foods."
    )

nutrition_expert_agent = Agent(
    name="NutritionExpertAgent",
    instructions="Offer dietary advice for users with medical conditions using the tool.",
    tools=[nutrition_expert_tool],
)
