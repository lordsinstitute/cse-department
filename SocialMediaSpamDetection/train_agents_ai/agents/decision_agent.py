import google.generativeai as genai
from train_agents_ai.config import MODEL_NAME

model = genai.GenerativeModel(MODEL_NAME)

def final_decision(content_result, behavior_result, link_result):

    prompt = f"""
    You are the final spam detection agent.

    Combine results from multiple agents
    and determine if the tweet is spam.

    Content Agent:
    {content_result}

    Behavior Agent:
    {behavior_result}

    Link Agent:
    {link_result}

    Return JSON:
    {{
        "label": "Spam" or "Quality",
        "confidence": 0-1,
        "reason": explanation
    }}
    """

    response = model.generate_content(prompt)

    return response.text