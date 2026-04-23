"""AI form filler agent."""

import json
from core.agents.base_agent import BaseAgent
from core.llm.prompts import FORM_FILLER_SYSTEM_PROMPT
from core.llm.tools import FORM_FILLER_TOOLS


class FormFillerAgent(BaseAgent):
    """Agent that fills web forms using resume data."""

    def __init__(self, resume_data, socketio=None, room=None):
        super().__init__(socketio=socketio, room=room)
        self.resume_data = resume_data

    def get_system_prompt(self):
        data_str = json.dumps(self.resume_data, indent=2)
        return FORM_FILLER_SYSTEM_PROMPT.format(resume_data=data_str)

    def get_tools(self):
        return FORM_FILLER_TOOLS
