from agents import Agent, GuardrailFunctionOutput, RunContextWrapper
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

# 👤 Nutrition Expert Agent
nutrition_expert_agent = Agent[UserSessionContext](
    name="NutritionExpertAgent",
    model="gpt-4o-mini",
    instructions="Provide dietary advice based on user dietary restrictions or health conditions."
)
