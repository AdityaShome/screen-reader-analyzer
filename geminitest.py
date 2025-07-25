import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("AIzaSyDU3DOOqlPL3pWyXI03SkLIRKksWCXOPCk"))

model = genai.GenerativeModel('models/gemini-2.5-flash')
response = model.generate_content("Explain how AI works in a in 50 words")
print(response.text)