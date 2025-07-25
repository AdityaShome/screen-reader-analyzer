import sys
import time
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QLabel
)
from ocr import capture_and_extract_message
from analysis import analyze_message
from web_search import search_web
from reply_generator import generate_reply


class ChatResponderApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('WhatsApp Chat AI Responder')
        self.setGeometry(100, 100, 600, 400)
        layout = QVBoxLayout()

        self.info_label = QLabel(
            'Click "Capture Message" to read the latest WhatsApp message.'
        )
        layout.addWidget(self.info_label)

        self.capture_btn = QPushButton('Capture Message')
        self.capture_btn.clicked.connect(self.handle_capture)
        layout.addWidget(self.capture_btn)

        self.reply_area = QTextEdit()
        self.reply_area.setReadOnly(True)
        layout.addWidget(self.reply_area)

        self.setLayout(layout)

    def handle_capture(self):
        self.showMinimized()
        QApplication.processEvents()
        time.sleep(1)
        self.info_label.setText('Capturing message...')
        message = capture_and_extract_message()
        self.showNormal()
        QApplication.processEvents()
        print(f"DEBUG: Captured message: '{message}'")
        if not message:
            self.info_label.setText(
                'No message found. Make sure WhatsApp is visible.'
            )
            return
        self.info_label.setText('Analyzing message...')
        tone = analyze_message(message)
        print(f"DEBUG: Detected tone: {tone}")
        self.info_label.setText(f'Searching web for: "{message}"')
        web_info = search_web(message)
        print(f"DEBUG: Web info: {web_info}")
        self.info_label.setText('Generating reply...')
        reply = generate_reply(message, tone, web_info)
        print(f"DEBUG: Generated reply: {reply}")
        self.reply_area.setText(reply)
        self.info_label.setText('Reply generated!')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ChatResponderApp()
    window.show()
    sys.exit(app.exec_()) 