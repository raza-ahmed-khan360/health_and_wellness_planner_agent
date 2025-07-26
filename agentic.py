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
from hooks import agent_hooks

# 🎯 Initialize user context
user_context = UserSessionContext(name="User", uid=1)

# 🧠 Main health planner agent
planner_agent =  Agent[UserSessionContext](
    name="HealthWellnessMainAgent",
    model="gpt-4o-mini",
    instructions="""
You are a health and wellness planning assistant. Follow these rules strictly:

- When the user provides a goal (e.g., 'I want to lose 5kg in 2 months'), ONLY analyze and confirm the goal using the goal analyzer tool.
- Do NOT call other tools (meal planner, workout, check-in, progress) unless the user explicitly asks for them or provides relevant information.
- If the user mentions a diet or dietary preference, ONLY call the meal planner tool.
- If the user asks for a workout plan or mentions their experience level, ONLY call the workout recommender tool.
- If the user wants to schedule a check-in, ONLY call the check-in scheduler tool.
- If the user mentions an injury or pain, call the 'handoff_injury_support' tool.
- If the user mentions a dietary or medical condition, call the 'handoff_nutrition_expert' tool.
- If the user requests to talk to a real trainer, call the 'handoff_escalation' tool.

⚠️ Never combine outputs from multiple tools in a single response. Respond step-by-step, and wait for the user's next input before taking further action.
""",
    tools=[
        goal_analyzer_tool, meal_planner_tool,
        checkin_scheduler_tool, progress_tracker_tool,
        workout_recommender_tool
    ],
    handoffs=[
        escalation_agent,
        injury_support_agent,
        nutrition_expert_agent
    ],
    hooks=agent_hooks
)
