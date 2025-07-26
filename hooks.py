from typing import Any
from agents import Agent, Tool, RunHooks, AgentHooks, RunContextWrapper
from context import UserSessionContext

# 🔄 Global lifecycle hooks
class LoggingRunHooks(RunHooks[UserSessionContext]):
    async def on_agent_start(self, context: RunContextWrapper[UserSessionContext], agent: Agent) -> None:
        print(f"[RUN HOOK] 🔄 Agent '{agent.name}' is starting.")

    async def on_agent_end(self, context: RunContextWrapper[UserSessionContext], agent: Agent, output: Any) -> None:
        print(f"[RUN HOOK] ✅ Agent '{agent.name}' ended with output:")
        print(output)

    async def on_tool_start(self, context: RunContextWrapper[UserSessionContext], agent: Agent, tool: Tool) -> None:
        tool_input = getattr(tool, "input", "N/A")
        print(f"[RUN HOOK] 🔧 Agent '{agent.name}' is invoking tool '{tool.name}' with input: {tool_input}")

    async def on_tool_end(self, context: RunContextWrapper[UserSessionContext], agent: Agent, tool: Tool, result: Any) -> None:
        print(f"[RUN HOOK] 📦 Tool '{tool.name}' returned:")
        print(result)

    async def on_handoff(self, context: RunContextWrapper[UserSessionContext], from_agent: Agent, to_agent: Agent) -> None:
        print(f"[RUN HOOK] 🔁 Handoff from agent '{from_agent.name}' to '{to_agent.name}'.")

    async def on_error(self, context: RunContextWrapper[UserSessionContext], agent: Agent, error: Exception) -> None:
        print(f"[RUN HOOK] ❌ Error in agent '{agent.name}': {error}")


# 🧠 Intent-based tool selection guard
def get_expected_tool(user_input: str) -> str | None:
    user_input = user_input.lower()
    if any(word in user_input for word in ["goal", "lose", "gain", "drop", "shed", "put on"]):
        return "goal_analyzer_tool"
    elif any(word in user_input for word in ["meal", "diet", "vegetarian", "keto", "nutrition"]):
        return "meal_planner_tool"
    elif any(word in user_input for word in ["workout", "exercise", "fitness", "training"]):
        return "workout_recommender_tool"
    elif any(word in user_input for word in ["check-in", "checkin", "remind", "schedule"]):
        return "checkin_scheduler_tool"
    elif any(word in user_input for word in ["progress", "track", "log weight"]):
        return "progress_tracker_tool"
    elif any(word in user_input for word in ["injury", "pain", "hurt"]):
        return "handoff_injury_support"
    elif any(word in user_input for word in ["medical", "condition", "diabetes", "cholesterol"]):
        return "handoff_nutrition_expert"
    elif any(word in user_input for word in ["real trainer", "human", "expert"]):
        return "handoff_escalation"
    return None


# 🤖 Agent-specific lifecycle hooks
class LoggingAgentHooks(AgentHooks[UserSessionContext]):
    async def on_start(self, context: RunContextWrapper[UserSessionContext], agent: Agent) -> None:
        print(f"[AGENT HOOK] ▶️ Agent '{agent.name}' is starting.")

    async def on_end(self, context: RunContextWrapper[UserSessionContext], agent: Agent, output: Any) -> None:
        print(f"[AGENT HOOK] 🛑 Agent '{agent.name}' finished with output:")
        print(output)

    async def on_tool_start(self, context: RunContextWrapper[UserSessionContext], agent: Agent, tool: Tool) -> None:
        tool_input = getattr(tool, "input", "N/A")
        print(f"[AGENT HOOK] 🧰 Tool '{tool.name}' started by '{agent.name}' with input: {tool_input}")

    async def on_tool_end(self, context: RunContextWrapper[UserSessionContext], agent: Agent, tool: Tool, result: Any) -> None:
        print(f"[AGENT HOOK] ✅ Tool '{tool.name}' ended with result:")
        print(result)

    async def on_handoff(self, context: RunContextWrapper[UserSessionContext], from_agent: Agent, to_agent: Agent) -> None:
        print(f"[AGENT HOOK] 🔄 Handoff from '{from_agent.name}' to '{to_agent.name}'.")

    # ✅ Guardrail: restrict which tool can be called based on user input
    async def before_tool_call(self, tool_call: Any, context: UserSessionContext):
        expected_tool = get_expected_tool(context.last_user_input or "")
        tool_name = tool_call.tool.name

        if expected_tool and tool_name != expected_tool:
            raise Exception(
                f"❌ Tool '{tool_name}' was blocked. Based on your request, only '{expected_tool}' is permitted."
            )

# 🔌 Export hooks
run_hooks = LoggingRunHooks()
agent_hooks = LoggingAgentHooks()
