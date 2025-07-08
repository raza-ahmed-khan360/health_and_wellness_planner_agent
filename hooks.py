from agents import RunHooks, AgentHooks

class LoggingRunHooks(RunHooks):
    async def on_agent_start(self, context, agent):
        print(f"[HOOK] Agent '{agent.name}' is starting.")

    async def on_tool_end(self, context, agent, tool, result):
        print(f"[HOOK] Tool '{tool.name}' returned: {result}")

class LoggingAgentHooks(AgentHooks):
    async def on_start(self, context, agent):
        print(f"[AGENT HOOK] Starting agent: {agent.name}")

    async def on_end(self, context, agent, output):
        print(f"[AGENT HOOK] Agent '{agent.name}' finished with output: {output}")

# Export instances
run_hooks = LoggingRunHooks()
agent_hooks = LoggingAgentHooks()
