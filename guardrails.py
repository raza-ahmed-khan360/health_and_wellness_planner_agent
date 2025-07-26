import re
from typing import List, Union
from pydantic import BaseModel
from agents import input_guardrail, output_guardrail, GuardrailFunctionOutput

# --- 🥗 VALID DIET MAPPING ---
VALID_DIET_ALIASES = {
    "vegetarian": ["vegetarian", "veggie", "no meat", "plant-based"],
    "vegan": ["vegan", "strict vegan", "100% plant-based", "fully plant-based"],
    "keto": ["keto", "ketogenic", "low carb", "low-carb", "fat adapted"],
    "paleo": ["paleo", "paleolithic", "caveman diet"],
    "diabetic": ["diabetic", "diabetes friendly", "low sugar"],
    "gluten-free": ["gluten free", "gluten-free", "celiac", "no gluten"],
}

DIET_ALIASES = {alias: key for key, vals in VALID_DIET_ALIASES.items() for alias in vals}

def normalize_diet_name(name: str) -> str:
    cleaned = name.strip().lower()
    return DIET_ALIASES.get(cleaned, cleaned)

def is_valid_diet(name: str) -> bool:
    return normalize_diet_name(name) in VALID_DIET_ALIASES


# --- 🧠 GOAL VALIDATION ---
def is_valid_goal_format(text: str) -> bool:
    text = text.lower().strip()

    explicit_pattern = r"\b(?:lose|gain|drop|shed|put on|reduce|cut|add)?\s*\d+(?:\.\d+)?\s*(kg|kgs|kilograms?|pounds?|lbs?)\b"
    explicit_match = re.search(explicit_pattern, text)

    implicit_keywords = [
        "weight loss", "fat loss", "get fit", "tone up", "burn fat",
        "bulk up", "slim down", "gain muscle", "build muscle",
        "reduce weight", "shape up", "fitness", "lose weight",
        "cut weight", "gain weight", "get in shape", "build body"
    ]
    implicit_match = any(kw in text for kw in implicit_keywords)

    duration_pattern = r"\b(?:in|over|within)?\s*\d{1,2}\s*(day|days|week|weeks|month|months|year|years)\b"
    duration_match = re.search(duration_pattern, text)

    return bool((explicit_match or implicit_match) and duration_match)


def is_injury_related(text: str) -> bool:
    keywords = [
        "injury", "injured", "hurt", "pain", "ache", "sprain", "strain",
        "fracture", "sore", "twist", "dislocate", "broken", "swelling",
        "cramp", "bruise", "joint pain", "muscle pain", "knee pain",
        "back pain", "elbow pain", "ankle pain", "shoulder pain"
    ]
    return any(word in text.lower() for word in keywords)


# --- 📤 OUTPUT MODELS ---
class StructuredGoal(BaseModel):
    quantity: float
    metric: str
    duration: str

class MealPlanDay(BaseModel):
    day: str
    meal_name: str
    description: str
    calories: int


# --- ✅ INPUT GUARDRAILS ---
@input_guardrail
async def validate_goal_input(
    input: Union[str, List[dict]]
) -> GuardrailFunctionOutput:
    if isinstance(input, list):
        input = " ".join(m.get("content", "") for m in input if m.get("role") == "user")

    input = input.strip()
    if not input:
        return GuardrailFunctionOutput(
            output_info={"reason": "No goal provided."},
            tripwire_triggered=True
        )

    valid = is_valid_goal_format(input)

    return GuardrailFunctionOutput(
        output_info={
            "reason": "Goal format is valid." if valid else "Please specify a goal like 'lose 5kg in 2 months'."
        },
        tripwire_triggered=not valid
    )


@input_guardrail
async def validate_diet_input(
    input: Union[str, List[dict]]
) -> GuardrailFunctionOutput:
    if isinstance(input, list):
        input = " ".join(m.get("content", "") for m in input if m.get("role") == "user")

    input = input.strip()
    if not input:
        return GuardrailFunctionOutput(
            output_info={"reason": "No diet provided."},
            tripwire_triggered=True
        )

    norm = normalize_diet_name(input)
    valid = is_valid_diet(norm)

    return GuardrailFunctionOutput(
        output_info={
            "reason": "Diet preference recognized." if valid else f"'{input}' is not a supported diet.",
            "normalized_diet": norm
        },
        tripwire_triggered=not valid
    )


@input_guardrail
async def validate_injury_input(
    input: Union[str, List[dict]]
) -> GuardrailFunctionOutput:
    if isinstance(input, list):
        input = " ".join(m.get("content", "") for m in input if m.get("role") == "user")

    input = input.strip()
    if not input:
        return GuardrailFunctionOutput(
            output_info={"reason": "No input provided."},
            tripwire_triggered=False
        )

    detected = is_injury_related(input)

    return GuardrailFunctionOutput(
        output_info={
            "reason": "Injury-related input detected." if detected else "No injury indicators found.",
            "injury_detected": detected
        },
        tripwire_triggered=False
    )


# --- 📥 OUTPUT GUARDRAILS ---
@output_guardrail
async def validate_goal_output(
    output: any
) -> GuardrailFunctionOutput:
    is_valid = isinstance(output, StructuredGoal)

    return GuardrailFunctionOutput(
        output_info={
            "reason": "Goal output is valid." if is_valid else "Output is not a valid goal structure."
        },
        tripwire_triggered=not is_valid
    )


@output_guardrail
async def validate_mealplan_output(
    output: any
) -> GuardrailFunctionOutput:
    is_valid = isinstance(output, list) and all(isinstance(day, MealPlanDay) for day in output)

    return GuardrailFunctionOutput(
        output_info={
            "reason": "Meal plan structure is valid." if is_valid else "Meal plan must be a list of valid MealPlanDay items."
        },
        tripwire_triggered=not is_valid
    )


# --- ✅ EXPORT GUARDRAILS ---
goal_input = validate_goal_input
diet_input = validate_diet_input
injury_input = validate_injury_input
goal_output = validate_goal_output
mealplan_output = validate_mealplan_output


