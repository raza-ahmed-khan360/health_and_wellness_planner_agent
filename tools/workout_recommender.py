from agents.tool import function_tool
from pydantic import BaseModel
from typing import Literal, List, Optional
from agents import RunContextWrapper
from context import UserSessionContext

# 🏋️ Input model
class WorkoutInput(BaseModel):
    experience_level: str  # Accept freeform input

# 📅 Output model
class WorkoutDay(BaseModel):
    day: str
    workout: str
    duration_minutes: int

# ✅ Streaming-compatible tool with context wrapper
@function_tool("WorkoutRecommenderTool")
async def workout_recommender_tool(
    wrapper: RunContextWrapper[UserSessionContext],
    inputs: WorkoutInput
) -> Optional[List[WorkoutDay]]:
    raw_level = inputs.experience_level.strip().lower()

    synonyms = {
        "beginner": ["beginner", "newbie", "just started", "starting out"],
        "intermediate": ["intermediate", "some experience", "moderate"],
        "advanced": ["advanced", "expert", "pro", "very experienced"]
    }

    # Normalize experience level
    level = next((key for key, values in synonyms.items() if raw_level in values), None)
    if not level:
        wrapper.context.workout_plan = None
        return None

    # Workout schedule & durations
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

    week_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    plan = [
        WorkoutDay(
            day=day,
            workout=weekly_schedule[level][i],
            duration_minutes=durations[level]
        )
        for i, day in enumerate(week_days)
    ]

    # Update context
    wrapper.context.workout_plan = [p.model_dump() for p in plan]
    return plan
