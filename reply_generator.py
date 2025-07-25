import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
gemini_api_key = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=gemini_api_key)


def generate_reply(message, tone, web_info):
    prompt = (
        f"You are an assistant replying to a WhatsApp message. "
        f"The message is: '{message}'.\n"
        f"The desired tone is: {tone}.\n"
        f"Here is some latest info from the web: {web_info}.\n"
        f"Compose a reply in the specified tone, using the web info if "
        f"relevant. Keep it concise and natural."
    )
    try:
        model = genai.GenerativeModel('models/gemini-2.5-flash')
        response = model.generate_content(prompt)
        reply = response.text.strip()
        return reply
    except Exception as e:
        print(f"Gemini API error: {e}")
        return (
            f"[{tone.upper()}] {web_info} "
            f"(in reply to: {message})"
        ) 