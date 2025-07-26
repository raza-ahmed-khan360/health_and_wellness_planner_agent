from agents import function_tool, RunContextWrapper
from context import UserSessionContext
from pydantic import BaseModel
from typing import List, Optional

# 🏋️ Input model
class WorkoutInput(BaseModel):
    experience_level: str  # Freeform input like "beginner", "just started", etc.

# 📅 Output model
class WorkoutDay(BaseModel):
    day: str
    workout: str
    duration_minutes: int

# 🛠️ Final tool definition
@function_tool
async def workout_recommender_tool(
    wrapper: RunContextWrapper[UserSessionContext],
    inputs: WorkoutInput
) -> str:
    raw_level = inputs.experience_level.strip().lower()

    # Mapping freeform input to canonical levels
    synonyms = {
        "beginner": ["beginner", "newbie", "just started", "starting out"],
        "intermediate": ["intermediate", "some experience", "moderate"],
        "advanced": ["advanced", "expert", "pro", "very experienced"]
    }

    # Normalize input
    level = next((key for key, values in synonyms.items() if raw_level in values), None)
    if not level:
        wrapper.context.workout_plan = None
        return "❌ Sorry, I couldn't recognize your experience level."

    # Weekly workout templates
    weekly_schedule = {
        "beginner":     ["Full-body light", "Walk", "Rest", "Yoga", "Light strength", "Rest", "Cardio"],
        "intermediate": ["Push", "Pull", "Legs", "Cardio", "Yoga", "Rest", "Full-body"],
        "advanced":     ["Push + Cardio", "Pull + Abs", "Legs + Core", "HIIT", "Active Recovery", "Strength Split", "Endurance"]
    }

    durations = {
        "beginner": 30,
        "intermediate": 45,
        "advanced": 60
    }

    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    plan = [
        WorkoutDay(
            day=day,
            workout=weekly_schedule[level][i],
            duration_minutes=durations[level]
        )
        for i, day in enumerate(days)
    ]

    wrapper.context.workout_plan = [entry.model_dump() for entry in plan]

    # Format as Markdown
    markdown = [f"Here's a {level} workout plan for the week:\n"]
    for entry in plan:
        markdown.append(f"- **{entry.day}:** {entry.workout}  ")
        markdown.append(f"  _Duration:_ {entry.duration_minutes} minutes")
    return "\n".join(markdown)
