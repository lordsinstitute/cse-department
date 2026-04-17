import google.generativeai as genai

GEMINI_API_KEY = "AIzaSyDyZZVUez7uQJd6_5965gSXhZhkg3bxbVg"

genai.configure(api_key=GEMINI_API_KEY)

MODEL_NAME = "gemini-2.5-flash"