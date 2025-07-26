import asyncio
import config
from agents import Runner, Agent, RunContextWrapper
from agents.exceptions import InputGuardrailTripwireTriggered
from context import UserSessionContext
from guardrails import goal_input, diet_input, injury_input
from tools import (
    goal_analyzer_tool, meal_planner_tool,
    checkin_scheduler_tool, progress_tracker_tool,
    workout_recommender_tool
)
from agent import (
    escalation_agent, injury_support_agent,
    nutrition_expert_agent, handoff_injury_support,
    handoff_nutrition_expert, handoff_escalation
)
from hooks import run_hooks, agent_hooks
from utils.streaming import stream_agent_output

session_context = UserSessionContext(name="User", uid=1)

planner_agent = Agent[UserSessionContext](
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
        workout_recommender_tool,
        handoff_injury_support, handoff_nutrition_expert, handoff_escalation
    ],
    hooks=agent_hooks
)


async def main():
    print("🧠 Welcome to Health & Wellness CLI!")
    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() in ("exit", "quit"):
            print("👋 Goodbye!")
            break

        print("\n🤖 Agent:\n", end="", flush=True)
        try:
            async for chunk in stream_agent_output(
                planner_agent,
                user_input,
                session_context,
                hooks=run_hooks
            ):
                print(chunk, end="", flush=True)

            print("\n" + "="*50 + "\n")  # Better separation between turns

        except InputGuardrailTripwireTriggered as e:
            info = e.guardrail_result.output
            reason = info.get("reason") if isinstance(info, dict) else getattr(info, "reason", "Invalid input.")
            print(f"\n⚠️ Guardrail Blocked: {reason}\n")


if __name__ == "__main__":
    asyncio.run(main())
