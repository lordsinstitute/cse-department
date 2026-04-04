"""Web data extraction agent."""

from core.agents.base_agent import BaseAgent
from core.llm.prompts import SCRAPER_SYSTEM_PROMPT
from core.llm.tools import BROWSER_TOOLS


class ScraperAgent(BaseAgent):
    """Agent that extracts structured data from web pages."""

    def __init__(self, socketio=None, room=None):
        super().__init__(socketio=socketio, room=room)
        self.collected_data = []

    def get_system_prompt(self):
        return SCRAPER_SYSTEM_PROMPT

    def get_tools(self):
        return BROWSER_TOOLS

    def handle_extract_data(self, data, description):
        """Collect extracted data."""
        if isinstance(data, list):
            self.collected_data.extend(data)
        else:
            self.collected_data.append(data)
        self.emit_log(
            f"Total collected: {len(self.collected_data)} items", "success"
        )
