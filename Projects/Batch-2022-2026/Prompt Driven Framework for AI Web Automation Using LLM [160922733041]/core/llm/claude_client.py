"""Claude API wrapper with tool use support."""

import time
import anthropic
from config import Config


class ClaudeClient:
    """Wrapper around the Anthropic API for tool-use conversations."""

    def __init__(self):
        self.client = anthropic.Anthropic(api_key=Config.ANTHROPIC_API_KEY)
        self.model = Config.CLAUDE_MODEL

    def think(self, system_prompt, messages, tools):
        """Send state to Claude and get back a tool-use action.

        Args:
            system_prompt: System prompt string
            messages: List of message dicts (role/content)
            tools: List of tool definition dicts

        Returns:
            dict with keys: action, action_input, thinking, tool_use_id, raw_response
        """
        for attempt, delay in enumerate(Config.RATE_LIMIT_DELAYS + [None]):
            try:
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=4096,
                    system=system_prompt,
                    messages=messages,
                    tools=tools,
                )
                return self._parse_response(response)
            except anthropic.RateLimitError:
                if delay is None:
                    raise
                time.sleep(delay)
            except anthropic.APIError as e:
                if attempt < len(Config.RATE_LIMIT_DELAYS) and "overloaded" in str(e).lower():
                    time.sleep(Config.RATE_LIMIT_DELAYS[attempt])
                else:
                    raise

    def _parse_response(self, response):
        """Parse Claude's response to extract tool use."""
        result = {
            "action": None,
            "action_input": {},
            "thinking": "",
            "tool_use_id": None,
            "raw_response": response,
        }

        for block in response.content:
            if block.type == "text":
                result["thinking"] = block.text
            elif block.type == "tool_use":
                result["action"] = block.name
                result["action_input"] = block.input
                result["tool_use_id"] = block.id

        # If Claude didn't use a tool, treat as done with failure
        if result["action"] is None and response.stop_reason == "end_turn":
            result["action"] = "done"
            result["action_input"] = {
                "summary": result["thinking"] or "Agent stopped without using a tool.",
                "success": False,
            }

        return result

    def build_tool_result_message(self, tool_use_id, result):
        """Build a tool_result message for conversation continuity."""
        return {
            "role": "user",
            "content": [
                {
                    "type": "tool_result",
                    "tool_use_id": tool_use_id,
                    "content": str(result),
                }
            ],
        }

    def parse_resume(self, system_prompt, resume_text, tool):
        """Parse a resume using forced tool choice.

        Args:
            system_prompt: System prompt
            resume_text: Resume text content
            tool: The save_resume_data tool definition

        Returns:
            Structured resume data dict
        """
        response = self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            system=system_prompt,
            messages=[{"role": "user", "content": resume_text}],
            tools=[tool],
            tool_choice={"type": "tool", "name": "save_resume_data"},
        )

        for block in response.content:
            if block.type == "tool_use":
                return block.input

        return {}
