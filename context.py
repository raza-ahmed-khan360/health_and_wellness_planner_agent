from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime

# 🎯 Goal Schema
class Goal(BaseModel):
    quantity: float
    metric: str  # e.g., "kg", "lbs"
    duration: str  # e.g., "2 months"

# 🍽️ Meal Plan Schema
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

# 📦 Shared session context
class UserSessionContext(BaseModel):
    name: str
    uid: int
    goal: Optional[Goal] = None
    diet_preferences: Optional[str] = None
    workout_plan: List[WorkoutDay] = Field(default_factory=list)
    meal_plan: List[MealPlanDay] = Field(default_factory=list)
    injury_notes: Optional[str] = None
    handoff_logs: List[str] = Field(default_factory=list)
    progress_logs: List[Dict[str, str]] = Field(default_factory=list)
    checkin_schedule: List[Dict[str, str]] = Field(default_factory=list)
    last_user_input: Optional[str] = None  
