"""Base agent with the observe-think-act loop."""

import time
import traceback
from core.browser.manager import BrowserManager
from core.browser.page_state import extract_page_state, format_state_for_llm
from core.browser.actions import execute_action
from core.llm.client_factory import create_llm_client
from core.security import mask_sensitive
from config import Config


class BaseAgent:
    """Base class for AI browser automation agents.

    Subclasses override:
        - get_system_prompt(): return the system prompt
        - get_tools(): return the tool definitions
        - handle_extract_data(data, description): process extracted data
    """

    def __init__(self, socketio=None, room=None):
        self.socketio = socketio
        self.room = room
        self.browser = BrowserManager()
        self.llm = create_llm_client()
        self.messages = []
        self.step = 0
        self.max_steps = Config.MAX_AGENT_STEPS
        self.step_delay = Config.STEP_DELAY
        self.consecutive_errors = 0
        self._stopped = False

    def get_system_prompt(self):
        raise NotImplementedError

    def get_tools(self):
        raise NotImplementedError

    def handle_extract_data(self, data, description):
        """Override to handle extracted data."""
        pass

    def stop(self):
        """Signal the agent to stop."""
        self._stopped = True

    def run(self, start_url, task_description):
        """Main agent loop: observe -> think -> act -> repeat.

        Returns:
            dict with 'success', 'summary', 'steps'
        """
        self.emit_log(f"Starting agent for: {task_description}", "info")
        result = {"success": False, "summary": "Agent did not complete.", "steps": 0}

        try:
            # Start browser and navigate
            self.browser.start()
            self.emit_log(f"Navigating to {start_url}...", "info")
            self.browser.new_page(start_url)
            self._take_screenshot()
            time.sleep(1)

            # Build initial message with task + page state
            state = self.browser.run_async(extract_page_state(self.browser.page))
            state_text = format_state_for_llm(state)

            self.messages = [
                {
                    "role": "user",
                    "content": f"Task: {task_description}\n\nCurrent page state:\n{state_text}",
                }
            ]

            # Agent loop
            while self.step < self.max_steps and not self._stopped:
                self.step += 1
                self.emit_log(f"Step {self.step}/{self.max_steps}", "info")

                # THINK: Ask Claude what to do
                try:
                    thought = self.llm.think(
                        self.get_system_prompt(),
                        self.messages,
                        self.get_tools(),
                    )
                except Exception as e:
                    self.emit_log(f"LLM error: {str(e)}", "error")
                    self.consecutive_errors += 1
                    if self.consecutive_errors >= Config.MAX_CONSECUTIVE_ERRORS:
                        result["summary"] = f"Too many LLM errors: {str(e)}"
                        break
                    continue

                action = thought["action"]
                action_input = thought["action_input"]
                thinking = thought.get("thinking", "")

                if thinking:
                    self.emit_log(f"Thinking: {thinking[:200]}", "thinking")

                # Handle done
                if action == "done":
                    summary = action_input.get("summary", "Task completed.")
                    success = action_input.get("success", True)
                    self.emit_log(f"Agent done: {summary}", "success" if success else "error")
                    result["success"] = success
                    result["summary"] = summary
                    result["steps"] = self.step
                    break

                # Handle extract_data
                if action == "extract_data":
                    data = action_input.get("data", [])
                    desc = action_input.get("description", "")
                    self.emit_log(f"Extracted {len(data)} items: {desc}", "action")
                    self.handle_extract_data(data, desc)

                    # Add assistant response and tool result to messages
                    self._append_assistant_response(thought)
                    tool_result = self.llm.build_tool_result_message(
                        thought["tool_use_id"],
                        f"Successfully extracted {len(data)} items."
                    )
                    self.messages.append(tool_result)

                    self._take_screenshot()
                    time.sleep(self.step_delay)
                    self._trim_messages()

                    # Re-observe and send state
                    state = self.browser.run_async(extract_page_state(self.browser.page))
                    state_text = format_state_for_llm(state)
                    self.messages.append({
                        "role": "user",
                        "content": f"Data extracted. Current page state:\n{state_text}",
                    })
                    self.consecutive_errors = 0
                    continue

                # ACT: Execute browser action
                self.emit_log(f"Action: {action}({_summarize_input(action_input)})", "action")

                action_result = self.browser.run_async(
                    execute_action(
                        self.browser.page,
                        action,
                        action_input,
                        state["elements"],
                    )
                )

                if action_result["success"]:
                    self.emit_log(f"Result: {action_result['message']}", "info")
                    self.consecutive_errors = 0
                else:
                    self.emit_log(f"Action failed: {action_result['message']}", "error")
                    self.consecutive_errors += 1

                if self.consecutive_errors >= Config.MAX_CONSECUTIVE_ERRORS:
                    result["summary"] = "Too many consecutive action errors."
                    self.emit_log(result["summary"], "error")
                    break

                # Add assistant response and tool result to messages
                self._append_assistant_response(thought)
                tool_result = self.llm.build_tool_result_message(
                    thought["tool_use_id"],
                    action_result["message"]
                )
                self.messages.append(tool_result)

                # Take screenshot after action
                time.sleep(self.step_delay)
                self._take_screenshot()

                # OBSERVE: Re-extract state
                state = self.browser.run_async(extract_page_state(self.browser.page))
                state_text = format_state_for_llm(state)

                self.messages.append({
                    "role": "user",
                    "content": f"Action result: {action_result['message']}\n\nCurrent page state:\n{state_text}",
                })

                self._trim_messages()

            else:
                if self._stopped:
                    result["summary"] = "Agent was stopped by user."
                    self.emit_log("Agent stopped by user.", "info")
                else:
                    result["summary"] = f"Reached max steps ({self.max_steps})."
                    self.emit_log(result["summary"], "error")
                result["steps"] = self.step

        except Exception as e:
            result["summary"] = f"Agent error: {str(e)}"
            self.emit_log(f"Error: {str(e)}", "error")
            traceback.print_exc()
        finally:
            try:
                self.browser.stop()
            except Exception:
                pass

        return result

    def _append_assistant_response(self, thought):
        """Add Claude's raw response to message history."""
        content = []
        if thought.get("thinking"):
            content.append({"type": "text", "text": thought["thinking"]})
        if thought.get("action") and thought.get("tool_use_id"):
            content.append({
                "type": "tool_use",
                "id": thought["tool_use_id"],
                "name": thought["action"],
                "input": thought["action_input"],
            })
        if content:
            self.messages.append({"role": "assistant", "content": content})

    def _trim_messages(self):
        """Keep conversation manageable while preserving tool_use/tool_result pairs.

        Messages come in triplets after the first:
          assistant (tool_use) → user (tool_result) → user (page state)
        We must never break this triplet apart.
        """
        if len(self.messages) <= 8:
            return

        # Keep first message (task + initial state), then find safe cut
        # A safe cut is at a "user" message with role=user and plain string content
        # (i.e., a page state message, NOT a tool_result)
        # We want to keep the last ~6 messages from the rest

        rest = self.messages[1:]
        target_keep = min(6, len(rest))
        cut = len(rest) - target_keep

        # Scan forward from cut to find a user message with plain string content
        # (a page-state message that starts a clean group)
        while cut < len(rest):
            msg = rest[cut]
            is_plain_user = (
                msg.get("role") == "user"
                and isinstance(msg.get("content"), str)
            )
            if is_plain_user:
                break
            cut += 1

        if cut >= len(rest):
            return  # can't safely trim

        self.messages = self.messages[:1] + rest[cut:]

    def _take_screenshot(self):
        """Take screenshot and emit via SocketIO."""
        try:
            screenshot = self.browser.screenshot(quality=Config.SCREENSHOT_QUALITY)
            if screenshot and self.socketio and self.room:
                self.socketio.emit("screenshot", {"image": screenshot}, room=self.room)
        except Exception:
            pass

    def emit_log(self, message, level="info"):
        """Emit a log message via SocketIO (with sensitive data masked)."""
        message = mask_sensitive(message)
        print(f"[{level.upper()}] {message}")
        if self.socketio and self.room:
            self.socketio.emit(
                "agent_log",
                {"message": message, "level": level, "step": self.step},
                room=self.room,
            )


def _summarize_input(action_input):
    """Create a short summary of action input for logging."""
    parts = []
    for k, v in action_input.items():
        if k == "reason":
            continue
        val = str(v)
        if len(val) > 50:
            val = val[:50] + "..."
        parts.append(f"{k}={val}")
    return ", ".join(parts)
