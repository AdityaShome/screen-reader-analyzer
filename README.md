# WhatsApp Chat AI Responder

A Windows GUI app that reads WhatsApp chat messages from your screen, analyzes them, uses AI to surf the web for the latest information, and generates suitable replies (informative, funny, or romantic).

## Features
- Reads WhatsApp chat messages from your screen using OCR
- Analyzes message intent (informative, funny, romantic)
- Uses OpenAI API to generate replies
- Searches the web for the latest information
- Displays the reply in a user-friendly GUI

## Setup
1. Install Python 3.8+
2. Clone this repository
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Install Tesseract OCR engine (required for pytesseract):
   - [Download for Windows](https://github.com/tesseract-ocr/tesseract/wiki)
   - Add Tesseract to your PATH
5. Get OpenAI API key and (optionally) SerpAPI key for web search

## Usage
- Run the app:
  ```
  python main.py
  ```
- Select the WhatsApp window and click 'Capture Message'
- The app will analyze the message, search the web, and display a suitable reply

---

**Note:** This app does not auto-send replies. It only displays them for you to copy and use. 