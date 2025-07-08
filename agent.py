import sys, os
sys.path.append(os.path.dirname(__file__))

from agents import Agent
from agents import injury_support_agent, nutrition_expert_agent, escalation_agent
from context import UserSessionContext, RunContextWrapper
from tools import goal_analyzer_tool, meal_planner_tool, workout_recommender_tool, checkin_scheduler_tool, progress_tracker_tool 

# Initial context
user_context = RunContextWrapper(UserSessionContext(name="User", uid=1))
planner_agent = Agent(
    name="HealthPlannerAgent",
    instructions="You are a health assistant. Collect user goals and preferences and suggest plans.",
    tools=[
        goal_analyzer_tool,
        meal_planner_tool,
        workout_recommender_tool,
        checkin_scheduler_tool,
        progress_tracker_tool
    ],
    handoffs=[
        injury_support_agent,
        nutrition_expert_agent,
        escalation_agent  
    ]
)

