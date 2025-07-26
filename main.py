import asyncio
import config
from agentic import (planner_agent, user_context)
from agents.exceptions import InputGuardrailTripwireTriggered
from hooks import run_hooks
from utils.streaming import stream_agent_output

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
                user_context,
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
