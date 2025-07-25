import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
gemini_api_key = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=gemini_api_key)


def analyze_message(message):
    prompt = (
        "Classify the following WhatsApp message as 'informative', 'funny', "
        "or 'romantic'. Only reply with one of these three words.\n\n"
        f"Message: {message}"
    )
    try:
        model = genai.GenerativeModel('models/gemini-2.5-flash')
        response = model.generate_content(prompt)
        tone = response.text.strip().lower()
        if tone in ['informative', 'funny', 'romantic']:
            return tone
        return 'informative'
    except Exception as e:
        print(f"Gemini API error: {e}")
        return 'informative' 