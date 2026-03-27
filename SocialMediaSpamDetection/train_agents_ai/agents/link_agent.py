import google.generativeai as genai
from train_agents_ai.config import MODEL_NAME

model = genai.GenerativeModel(MODEL_NAME)

def analyze_links(tweet):

    prompt = f"""
    Determine if this tweet contains suspicious links
    or scam marketing patterns.

    Tweet:
    {tweet}

    Return JSON:

    {{
        "spam_score": number between 0 and 1,
        "reason": explanation
    }}
    """

    response = model.generate_content(prompt)

    return response.text