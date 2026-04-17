import google.generativeai as genai
from train_agents_ai.config import MODEL_NAME

model = genai.GenerativeModel(MODEL_NAME)

def analyze_content(tweet):

    prompt = f"""
    You are a spam detection agent.

    Analyze the tweet below and determine if the language
    appears spammy.

    Look for:
    - promotional language
    - scams
    - repeated hashtags
    - suspicious marketing

    Tweet:
    {tweet}

    Return only JSON:
    {{
        "spam_score": number between 0 and 1,
        "reason": short explanation
    }}
    """

    response = model.generate_content(prompt)

    return response.text