from agents import Agent
import config
from agent import (
    injury_support_agent,
    nutrition_expert_agent,
    escalation_agent
)
from context import UserSessionContext
from tools import (
    goal_analyzer_tool,
    meal_planner_tool,
    workout_recommender_tool,
    checkin_scheduler_tool,
    progress_tracker_tool
)

# 🎯 Initialize user context
user_context = UserSessionContext(name="User", uid=1)

# 🧠 Main health planner agent
planner_agent = Agent[UserSessionContext](
    name="HealthPlannerAgent",
    model="openai:gpt-4o",
    instructions="You are a friendly and knowledgeable health assistant. Collect user goals and preferences, validate them, and suggest plans using your tools.",
    tools=[
        goal_analyzer_tool,
        meal_planner_tool,
        workout_recommender_tool,
        checkin_scheduler_tool,
        progress_tracker_tool,
    ],
    handoffs=[
        nutrition_expert_agent,
        injury_support_agent,
        escalation_agent
    ]
)
