"""Claude tool definitions for browser automation."""

BROWSER_TOOLS = [
    {
        "name": "click",
        "description": (
            "Click on an interactive element on the page. "
            "Use this to click links, buttons, checkboxes, radio buttons, etc."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "element_id": {
                    "type": "integer",
                    "description": "The ID number of the element to click (from the elements list)",
                },
                "reason": {
                    "type": "string",
                    "description": "Brief explanation of why you're clicking this element",
                },
            },
            "required": ["element_id", "reason"],
        },
    },
    {
        "name": "fill",
        "description": (
            "Fill a text input or textarea with a value. "
            "This will clear any existing value and type the new one."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "element_id": {
                    "type": "integer",
                    "description": "The ID number of the input/textarea element",
                },
                "value": {
                    "type": "string",
                    "description": "The text value to fill in",
                },
            },
            "required": ["element_id", "value"],
        },
    },
    {
        "name": "select_option",
        "description": (
            "Select an option from a dropdown/select element. "
            "Use the value attribute of the option you want to select."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "element_id": {
                    "type": "integer",
                    "description": "The ID number of the select element",
                },
                "value": {
                    "type": "string",
                    "description": "The value attribute of the option to select",
                },
            },
            "required": ["element_id", "value"],
        },
    },
    {
        "name": "navigate",
        "description": "Navigate the browser to a new URL.",
        "input_schema": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "The URL to navigate to",
                },
            },
            "required": ["url"],
        },
    },
    {
        "name": "scroll",
        "description": "Scroll the page up or down to see more content.",
        "input_schema": {
            "type": "object",
            "properties": {
                "direction": {
                    "type": "string",
                    "enum": ["up", "down"],
                    "description": "Direction to scroll",
                },
            },
            "required": ["direction"],
        },
    },
    {
        "name": "extract_data",
        "description": (
            "Extract structured data from the current page. Use this when you've found "
            "the data the user requested. Call this tool with the extracted data as a list "
            "of objects. You can call this multiple times if data spans multiple pages."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "data": {
                    "type": "array",
                    "items": {"type": "object"},
                    "description": "Array of extracted data objects (each object is one row)",
                },
                "description": {
                    "type": "string",
                    "description": "Brief description of what data was extracted",
                },
            },
            "required": ["data", "description"],
        },
    },
    {
        "name": "done",
        "description": (
            "Signal that the task is complete. Call this when you have finished "
            "the user's request or when you cannot proceed further."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "summary": {
                    "type": "string",
                    "description": "Summary of what was accomplished",
                },
                "success": {
                    "type": "boolean",
                    "description": "Whether the task was completed successfully",
                },
            },
            "required": ["summary", "success"],
        },
    },
]

# Form filler doesn't need extract_data
FORM_FILLER_TOOLS = [t for t in BROWSER_TOOLS if t["name"] != "extract_data"]

# Tool for resume parsing
RESUME_PARSE_TOOL = {
    "name": "save_resume_data",
    "description": "Save the structured resume data extracted from the document.",
    "input_schema": {
        "type": "object",
        "properties": {
            "full_name": {"type": "string", "description": "Full name of the candidate"},
            "email": {"type": "string", "description": "Email address"},
            "phone": {"type": "string", "description": "Phone number"},
            "address": {"type": "string", "description": "Physical address or location"},
            "summary": {"type": "string", "description": "Professional summary or objective"},
            "education": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "degree": {"type": "string"},
                        "institution": {"type": "string"},
                        "year": {"type": "string"},
                    },
                },
                "description": "Education history",
            },
            "experience": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "company": {"type": "string"},
                        "duration": {"type": "string"},
                        "description": {"type": "string"},
                    },
                },
                "description": "Work experience",
            },
            "skills": {
                "type": "array",
                "items": {"type": "string"},
                "description": "List of skills",
            },
        },
        "required": ["full_name", "email"],
    },
}
