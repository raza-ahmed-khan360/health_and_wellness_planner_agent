from agents import Agent, InputGuardrail, GuardrailFunctionOutput, RunContextWrapper, function_tool
from pydantic import BaseModel
from context import UserSessionContext
from guardrails import normalize_diet_name, is_valid_diet

# 🥗 Input schema
class NutritionInput(BaseModel):
    condition: str  # Diet or medical condition

# 🔒 Guardrail
async def nutrition_input_guardrail(
    ctx: RunContextWrapper[UserSessionContext],
    agent,
    input_text: str
) -> GuardrailFunctionOutput:
    normalized = normalize_diet_name(input_text)
    is_valid = is_valid_diet(normalized)
    return GuardrailFunctionOutput(
        output_info={
            "valid": is_valid,
            "reason": "Diet/condition recognized." if is_valid else f"'{input_text}' is not a supported diet or condition."
        },
        tripwire_triggered=not is_valid
    )

# 🧠 Route handler
async def handle_nutrition(ctx: RunContextWrapper[UserSessionContext], input_text: str) -> str:
    ctx.context.handoff_logs.append(f"NutritionExpertAgent consulted for: {input_text}")
    return (
        f"🥗 Thanks for mentioning '{input_text}'. "
        "I'll ensure all meal plans respect those dietary needs—avoiding restricted items, "
        "encouraging whole foods, and maintaining balanced nutrition."
    )

# 👤 Nutrition Expert Agent
nutrition_expert_agent = Agent[UserSessionContext](
    name="NutritionExpertAgent",
    model="gpt-4o-mini",
    instructions="Provide dietary advice based on user dietary restrictions or health conditions."
)

@function_tool
async def handoff_nutrition_expert(ctx: RunContextWrapper[UserSessionContext], input: str) -> str:
    return await handle_nutrition(ctx, input)
