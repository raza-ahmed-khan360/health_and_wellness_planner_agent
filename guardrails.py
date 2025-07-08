import re

# 🎯 Normalized diet types and synonyms
VALID_DIET_ALIASES = {
    "vegetarian": ["vegetarian", "veggie", "no meat", "plant-based no meat"],
    "vegan": ["vegan", "strict vegan", "100% plant-based", "fully plant-based"],
    "keto": ["keto", "ketogenic", "low carb", "low-carb", "fat adapted"],
    "paleo": ["paleo", "paleolithic", "caveman diet"],
    "diabetic": ["diabetic", "diabetes friendly", "low sugar"],
    "gluten-free": ["gluten free", "gluten-free", "celiac", "no gluten"],
}

# ✏️ Normalize diet name using mapping
DIET_ALIASES = {
    alias: key
    for key, values in VALID_DIET_ALIASES.items()
    for alias in values
}

# ✅ Utility: Normalize and validate diet
def normalize_diet_name(diet: str) -> str:
    return DIET_ALIASES.get(diet.lower().strip(), diet.lower().strip())

def is_valid_diet(diet: str) -> bool:
    return normalize_diet_name(diet) in VALID_DIET_ALIASES

# 🎯 Improved goal format validation (flexible)
def is_valid_goal_format(text: str) -> bool:
    text = text.lower()

    # Match quantity (5, 10.5, etc.)
    quantity_match = re.search(r"\b\d+(\.\d+)?\b", text)

    # Match units
    metric_match = re.search(r"\b(kilo|kilos|kg|kgs|pound|pounds|lbs|lb)\b", text)

    # Match durations like “in 2 months” or “over 3 weeks”
    duration_match = re.search(r"\b(in|over)?\s*(\d+)\s*(day|week|month|year)s?\b", text)

    return all([quantity_match, metric_match, duration_match])

# 🔎 Injury detection keywords
INJURY_KEYWORDS = [
    "injury", "injured", "hurt", "hurting", "pain", "painful", "ache", "aching", "sore",
    "soreness", "stiff", "twisted", "fracture", "fractured", "sprain", "sprained",
    "swollen", "numb", "tingling", "dislocated", "can’t move", "can't move"
]

# 🔍 Common body parts affected by fitness injuries
BODY_PARTS = [
    "knee", "knees", "back", "lower back", "upper back", "neck",
    "shoulder", "shoulders", "arm", "elbow", "wrist", "hand",
    "leg", "hip", "ankle", "foot", "feet"
]

# ✅ Utility: Detect injury-related text
def is_injury_related(text: str) -> bool:
    text = text.lower()

    # Direct match
    if any(kw in text for kw in INJURY_KEYWORDS):
        return True

    # Indirect pattern match like "my ankle hurts"
    for part in BODY_PARTS:
        if re.search(rf"\b{part}\b.*(hurt|pain|sore|injur|fractur|twist|sprain|stiff|ache)", text):
            return True

    return False
