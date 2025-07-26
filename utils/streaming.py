from typing import AsyncGenerator
from agents import Runner, Agent
from openai.types.responses import ResponseTextDeltaEvent

async def stream_agent_output(
    agent: Agent,
    user_input: str,
    context: any,
    hooks=None
) -> AsyncGenerator[str, None]:
    """
    Stream full conversational flow from the agent, including:
      - Token-level LLM responses (raw_response_event)
      - Tool call events and outputs (run_item_stream_event)
      - Handoff notices (agent_updated_stream_event)
    """
    result = Runner.run_streamed(
        starting_agent=agent,
        input=user_input,
        context=context,
        hooks=hooks
    )

    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            yield event.data.delta
        elif event.type == "run_item_stream_event":
            # tool calls or message outputs
            item = event.item
            output = getattr(item, 'text', getattr(item, 'output', ''))
            
            # Only yield meaningful content, filter out technical details
            if output:
                output_str = str(output)
                
                # Skip technical details and object representations
                skip_patterns = [
                    "[RUN HOOK]", "[AGENT HOOK]", "[EVENT]", 
                    "tool_call_item", "tool_call_output_item", "message_output_item",
                    "quantity=", "metric=", "duration=",
                    "WorkoutDay(", "MealPlanDay(", "StructuredGoal(",
                    "CheckinConfirmation(", "message="
                ]
                
                # Check if output contains any skip patterns
                should_skip = any(pattern in output_str for pattern in skip_patterns)
                
                # Only show meaningful messages (like success confirmations)
                if not should_skip and output_str.strip():
                    # Clean up the output for better display
                    clean_output = output_str.strip()
                    if clean_output.startswith("✅") or clean_output.startswith("🥗") or clean_output.startswith("🩹") or clean_output.startswith("🚨"):
                        yield f"\n{clean_output}\n"
                    elif "scheduled" in clean_output or "logged" in clean_output or "generated" in clean_output:
                        yield f"\n{clean_output}\n"
                        
        elif event.type == "agent_updated_stream_event":
            # Only show agent switches if they're meaningful
            if "Handoff" in event.new_agent.name or "Expert" in event.new_agent.name:
                yield f"\n💡 Switched to {event.new_agent.name}\n"

