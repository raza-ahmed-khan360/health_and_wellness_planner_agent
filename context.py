from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime
from agents import RunContextWrapper


# 🎯 Goal Schema
class Goal(BaseModel):
    quantity: float
    metric: str  # e.g., "kg", "lbs"
    duration: str  # e.g., "2 months"


class MealPlanDay(BaseModel):
    day: str
    meal_name: str
    description: str
    calories: int

# 🏋️ Workout Schema
class WorkoutDay(BaseModel):
    day: str
    workout: str
    duration_minutes: int


# 💬 Message Log
class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())


# 📦 Shared user context
class UserSessionContext(BaseModel):
    name: str
    uid: int

    goal: Optional[dict] = None
    diet_preferences: Optional[str] = None
    workout_plan: Optional[dict] = None
    meal_plan: Optional[list] = None
    injury_notes: Optional[str] = None
    handoff_logs: List[str] = Field(default_factory=list)
    progress_logs: List[Dict[str, str]] = Field(default_factory=list)
    chat_history: List[ChatMessage] = Field(default_factory=list)
    checkin_schedule: Optional[List[Dict[str, str]]] = Field(default_factory=list)

# 🎒 OpenAI Agents SDK-compatible context wrapper
user_context = RunContextWrapper(UserSessionContext(
    name="User",
    uid=1
))
