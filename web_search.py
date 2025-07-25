import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
gemini_api_key = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=gemini_api_key)


def search_web(query):
    prompt = (
        f"You are a helpful assistant. Please provide the latest news or "
        f"information available on the following topic, as if you just "
        f"searched the web. Be concise and up-to-date.\n\nQuery: {query}"
    )
    try:
        model = genai.GenerativeModel('models/gemini-2.5-flash')
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Gemini API error: {e}")
        return "Could not retrieve latest info." 