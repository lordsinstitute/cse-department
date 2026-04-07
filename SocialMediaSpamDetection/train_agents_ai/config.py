import google.generativeai as genai

GEMINI_API_KEY = "AIzaSyDi3foeQSeHi9iKIsFHDds5Qm1t8fh9Bik"

genai.configure(api_key=GEMINI_API_KEY)

MODEL_NAME = "gemini-2.5-flash"