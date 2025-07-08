import asyncio
import config  

from agents import Runner, Agent
from context import UserSessionContext, RunContextWrapper
# Tools
from tools.goal_analyzer import goal_analyzer_tool
from tools.meal_planner import meal_planner_tool
from tools.scheduler import checkin_scheduler_tool
from tools.tracker import progress_tracker_tool
from tools.workout_recommender import workout_recommender_tool

# Specialized agents (for handoffs)
from agent.escalation_agent import escalation_agent
from agent.injury_support_agent import injury_support_agent
from agent.nutrition_expert_agent import nutrition_expert_agent

# Context and hooks
from hooks import run_hooks, agent_hooks
from utils.streaming import stream_agent_output
from context import user_context


# ✅ Declare the main agent
main_agent = Agent(
    name="HealthWellnessMainAgent",
    instructions=(
        "You are a smart, friendly health and wellness assistant. "
        "Help users define goals, suggest workouts, plan meals, schedule check-ins, and track progress. "
        "Use tools wisely and hand off to specialists when needed."
    ),
    tools=[
        goal_analyzer_tool,
        meal_planner_tool,
        checkin_scheduler_tool,
        progress_tracker_tool,
        workout_recommender_tool,
    ],
    handoffs=[
        escalation_agent,
        injury_support_agent,
        nutrition_expert_agent,
    ],
    hooks=agent_hooks,
)


# ✅ Main CLI loop
async def main():
    print("🧠 Welcome to your Health & Wellness Planner!")
    print("Type your goals, health info, or meal/workout requests. Type 'exit' to quit.\n")

    while True:
        user_input = input("👤 You: ")
        if user_input.strip().lower() in ["exit", "quit"]:
            print("👋 Goodbye! Stay healthy!")
            break

        print("🤖 AI:")

        # ✅ FIXED: Use Runner.stream(...) directly
        result = Runner.run_streamed(
            starting_agent=main_agent,
            input=user_input,
            context=user_context.context,
            hooks=run_hooks,
        )

        async for chunk in stream_agent_output(result):
            print(chunk, end="", flush=True)
        print("\n")


# ✅ Run event loop
if __name__ == "__main__":
    asyncio.run(main())
