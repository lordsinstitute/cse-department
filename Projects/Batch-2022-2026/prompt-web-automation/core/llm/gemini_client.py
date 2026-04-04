"""Google Gemini API wrapper with tool use support (using google-genai SDK)."""

import re
import time
from google import genai
from google.genai import types
from config import Config


class GeminiClient:
    """Wrapper around the Google Gemini API for tool-use conversations.

    Mirrors the ClaudeClient interface so agents can use either provider.
    """

    def __init__(self):
        self.client = genai.Client(api_key=Config.GEMINI_API_KEY)
        self.model_name = Config.GEMINI_MODEL
        self._tool_use_counter = 0

    def think(self, system_prompt, messages, tools):
        """Send state to Gemini and get back a tool-use action.

        Args:
            system_prompt: System prompt string
            messages: List of message dicts (Claude format: role/content)
            tools: List of tool definition dicts (Claude format)

        Returns:
            dict with keys: action, action_input, thinking, tool_use_id, raw_response
        """
        gemini_tools = self._convert_tools(tools)
        gemini_contents = self._convert_messages(messages)

        for attempt, delay in enumerate(Config.RATE_LIMIT_DELAYS + [None]):
            try:
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=gemini_contents,
                    config=types.GenerateContentConfig(
                        system_instruction=system_prompt,
                        tools=gemini_tools,
                        max_output_tokens=1024,
                    ),
                )
                return self._parse_response(response)
            except Exception as e:
                err_str = str(e).lower()
                if ("rate" in err_str or "quota" in err_str or "429" in err_str):
                    if delay is None:
                        raise
                    # Parse retry delay from error if available
                    retry_match = re.search(r'retry\s+(?:in|after)\s+(\d+)', err_str)
                    wait = int(retry_match.group(1)) if retry_match else delay
                    time.sleep(wait)
                elif "overloaded" in err_str or "503" in err_str:
                    if attempt < len(Config.RATE_LIMIT_DELAYS):
                        time.sleep(Config.RATE_LIMIT_DELAYS[attempt])
                    else:
                        raise
                else:
                    raise

    def _parse_response(self, response):
        """Parse Gemini's response to extract tool use."""
        result = {
            "action": None,
            "action_input": {},
            "thinking": "",
            "tool_use_id": None,
            "raw_response": response,
        }

        if not response.candidates:
            result["action"] = "done"
            result["action_input"] = {
                "summary": "No response from model.",
                "success": False,
            }
            return result

        candidate = response.candidates[0]

        for part in candidate.content.parts:
            if part.function_call:
                fc = part.function_call
                self._tool_use_counter += 1
                result["action"] = fc.name
                result["action_input"] = dict(fc.args) if fc.args else {}
                result["tool_use_id"] = f"gemini_tool_{self._tool_use_counter}"
            elif part.text:
                result["thinking"] = part.text

        # If no tool was called, treat as done
        if result["action"] is None:
            result["action"] = "done"
            result["action_input"] = {
                "summary": result["thinking"] or "Agent stopped without using a tool.",
                "success": False,
            }

        return result

    def build_tool_result_message(self, tool_use_id, result_text):
        """Build a tool_result message for conversation continuity.

        Returns Claude-format message (converted to Gemini format in _convert_messages).
        """
        return {
            "role": "user",
            "content": [
                {
                    "type": "tool_result",
                    "tool_use_id": tool_use_id,
                    "content": str(result_text),
                }
            ],
        }

    def parse_resume(self, system_prompt, resume_text, tool):
        """Parse a resume using Gemini with tool calling.

        Args:
            system_prompt: System prompt
            resume_text: Resume text content
            tool: The save_resume_data tool definition (Claude format)

        Returns:
            Structured resume data dict
        """
        gemini_tools = self._convert_tools([tool])

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=resume_text,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                tools=gemini_tools,
                max_output_tokens=4096,
            ),
        )

        if not response.candidates:
            return {}

        candidate = response.candidates[0]
        for part in candidate.content.parts:
            if part.function_call:
                return dict(part.function_call.args) if part.function_call.args else {}

        return {}

    def _convert_tools(self, claude_tools):
        """Convert Claude tool definitions to Gemini tool format."""
        declarations = []
        for tool in claude_tools:
            schema = tool.get("input_schema", {})
            declarations.append(types.FunctionDeclaration(
                name=tool["name"],
                description=tool.get("description", ""),
                parameters=self._clean_schema(schema),
            ))
        return [types.Tool(function_declarations=declarations)]

    def _clean_schema(self, schema):
        """Clean JSON schema for Gemini compatibility."""
        if not schema or not isinstance(schema, dict):
            return None

        cleaned = {}
        for key in ("type", "description", "enum", "required"):
            if key in schema:
                cleaned[key] = schema[key]

        if "properties" in schema:
            cleaned["properties"] = {
                k: self._clean_schema(v)
                for k, v in schema["properties"].items()
            }

        if "items" in schema:
            cleaned["items"] = self._clean_schema(schema["items"])

        return cleaned

    def _convert_messages(self, claude_messages):
        """Convert Claude-format messages to Gemini Content format."""
        gemini_contents = []

        for msg in claude_messages:
            role = "user" if msg["role"] == "user" else "model"
            content = msg["content"]

            if isinstance(content, str):
                gemini_contents.append(
                    types.Content(role=role, parts=[types.Part(text=content)])
                )
            elif isinstance(content, list):
                parts = []
                for block in content:
                    if isinstance(block, dict):
                        block_type = block.get("type", "")
                        if block_type == "text":
                            parts.append(types.Part(text=block["text"]))
                        elif block_type == "tool_use":
                            parts.append(types.Part(
                                function_call=types.FunctionCall(
                                    name=block["name"],
                                    args=block.get("input", {}),
                                )
                            ))
                        elif block_type == "tool_result":
                            parts.append(types.Part(
                                function_response=types.FunctionResponse(
                                    name="tool_response",
                                    response={"result": block.get("content", "")},
                                )
                            ))
                if parts:
                    gemini_contents.append(
                        types.Content(role=role, parts=parts)
                    )

        return gemini_contents
