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
    escalation_agent, injury_support_agent, nutrition_expert_agent,
    handoff_injury_support, handoff_nutrition_expert, handoff_escalation
)
from hooks import run_hooks, agent_hooks
from utils.streaming import stream_agent_output
import chainlit as cl

session_context = UserSessionContext(name="User", uid=1)

planner_agent = Agent[UserSessionContext](
    name="HealthWellnessMainAgent",
    model="gpt-4o-mini",
    instructions="""
As the Health and Wellness Planner Agent, your goal is to assist users in creating a personalized health and wellness plan. Utilize the provided tools to analyze goals, plan meals, schedule check-ins, track progress, and recommend workouts.

- If the user mentions an injury or pain, call the 'handoff_injury_support' tool.
- If the user mentions a dietary or medical condition, call the 'handoff_nutrition_expert' tool.
- If the user requests to talk to a real trainer, call the 'handoff_escalation' tool.
- If the user mentions a diet or dietary preference (e.g., vegetarian, vegan, keto), call the 'meal_planner_tool' to generate a meal plan.

⚠️ Never combine outputs from multiple tools in a single response.
""",
    tools=[
        goal_analyzer_tool, meal_planner_tool,
        checkin_scheduler_tool, progress_tracker_tool,
        workout_recommender_tool,
        handoff_injury_support, handoff_nutrition_expert, handoff_escalation
    ],
    hooks=agent_hooks
)

@cl.on_chat_start
async def start():
    await cl.Message(
        content=(
            "👋 **Welcome to your Health & Wellness Planner!**\n\n"
            "I'm here to help you build a custom plan.\n"
            "You can share your goals, diet preferences, or ask for workouts, meal plans, or progress tracking.\n\n"
            "_How can I assist you today?_"
        )
    ).send()

@cl.on_message
async def main(message: cl.Message):
    """Handle incoming messages"""
    user_input = message.content

    # Create a placeholder for streaming output
    msg = cl.Message(content="")
    await msg.send()

    try:
        # Stream the agent response
        async for chunk in stream_agent_output(planner_agent, user_input, session_context, hooks=run_hooks):
            if chunk.strip():  # Only stream non-empty chunks
                await msg.stream_token(chunk)

        # Finalize the streamed message
        await msg.update()

    except InputGuardrailTripwireTriggered as e:
        info = e.guardrail_result.output
        reason = info.get("reason") if isinstance(info, dict) else getattr(info, "reason", "Invalid input.")
        await cl.Message(
            content=f"⚠️ Guardrail triggered: {reason}",
            author="System"
        ).send()

    except Exception as e:
        await cl.Message(
            content=f"❌ Unexpected error: {str(e)}",
            author="System"
        ).send()
