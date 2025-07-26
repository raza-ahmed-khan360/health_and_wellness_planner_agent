import config
from agents.exceptions import InputGuardrailTripwireTriggered
from hooks import run_hooks
from agentic import planner_agent, user_context
from utils.streaming import stream_agent_output
import chainlit as cl

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
        async for chunk in stream_agent_output(planner_agent, user_input, user_context, hooks=run_hooks):
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
