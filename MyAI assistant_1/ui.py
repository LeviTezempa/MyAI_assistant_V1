from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTextEdit,
    QLineEdit,
    QPushButton,
)
from html import escape
from groq import GroqError
from calling import LocalAssistant
import pyttsx3 # text to speech
import speech_recognition as sr


class ChatApp(QWidget):
    def __init__(self, assistant):
        super().__init__()
        self.assistant = assistant
        self.engine = pyttsx3.init()
        self.recognizer = sr.Recognizer()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("MyAI Assistant")
        self.resize(650, 650)
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #f1f5f2, stop:1 #e8ebee);
                color: #1f2937;
                font-family: "Segoe UI", sans-serif;
            }
            QPushButton {
                border: none;
                background-color: #e9ecef;
                color: #111827;
            }
            QPushButton:hover {
                background-color: #dfe5ea;
            }
        """)

        root = QVBoxLayout(self)
        root.setContentsMargins(18, 16, 18, 18)
        root.setSpacing(12)

        self.chat_area = QTextEdit()
        self.chat_area.setReadOnly(True)
        self.chat_area.setPlaceholderText("")
        self.chat_area.setStyleSheet("""
            QTextEdit {
                background: rgba(255, 255, 255, 0.1);
                border: none;
                border-radius: 18px;
                padding: 12px;
                color: #1f2937;
                font-size: 15px;
            }
        """)
        self.chat_area.setMinimumHeight(410)
        root.addWidget(self.chat_area)

        input_wrap = QWidget()
        input_wrap.setFixedWidth(540)
        input_wrap.setStyleSheet("""
            QWidget {
                background: rgba(255, 255, 255, 0.72);
                border: 1px solid #d7dbe0;
                border-radius: 24px;
            }
        """)

        input_layout = QHBoxLayout(input_wrap)
        input_layout.setContentsMargins(10, 8, 10, 8)
        input_layout.setSpacing(8)

        self.mic_button = QPushButton("🎤")
        self.mic_button.setFixedSize(45, 45)
        self.mic_button.setStyleSheet("""
            QPushButton {
                border-radius: 22px;
                background-color: #e9ecef;
                color: #1f2937;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #dfe5ea;
            }
        """)
        self.mic_button.clicked.connect(self.listen_voice)

        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("Message")
        self.input_box.setMinimumHeight(45)
        self.input_box.setStyleSheet("""
            QLineEdit {
                background: transparent;
                border: none;
                color: #111827;
                font-size: 15px;
                padding: 0 10px;
            }
        """)
        self.input_box.returnPressed.connect(self.send_message)

        self.speaker_button = QPushButton("🔊")
        self.speaker_button.setFixedSize(45, 45)
        self.speaker_button.setStyleSheet("""
            QPushButton {
                border-radius: 22px;
                background-color: #e9ecef;
                color: #1f2937;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #dfe5ea;
            }
        """)
        self.speaker_button.clicked.connect(self.speak_response)

        self.send_button = QPushButton("Send")
        self.send_button.setFixedSize(78, 45)
        self.send_button.setStyleSheet("""
            QPushButton {
                border-radius: 16px;
                background-color: #e9ecef;
                color: #1f2937;
                font-size: 14px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #dfe5ea;
            }
        """)
        self.send_button.clicked.connect(self.send_message)

        input_layout.addWidget(self.mic_button)
        input_layout.addWidget(self.input_box)
        input_layout.addWidget(self.speaker_button)
        input_layout.addWidget(self.send_button)

        root.addWidget(input_wrap, alignment=Qt.AlignmentFlag.AlignHCenter)

    def append_message(self, sender, text):
        if not text:
            return

        bubble_style = (
            "background-color: #2f7af6; color: white; border-radius: 16px; "
            "padding: 10px 14px; margin: 6px 0; display: inline-block; "
            "max-width: 75%;"
            if sender == "user"
            else "background-color: #e5e7eb; color: #1f2937; border-radius: 16px; "
            "padding: 10px 14px; margin: 6px 0; display: inline-block; "
            "max-width: 75%;"
        )

        alignment = "right" if sender == "user" else "left"
        self.chat_area.append(
            f'<div style="text-align: {alignment}; margin: 4px 0;">'
            f'<span style="{bubble_style};">{escape(str(text))}</span></div>'
        )
        self.chat_area.verticalScrollBar().setValue(
            self.chat_area.verticalScrollBar().maximum()
        )

    def send_message(self):
        user_text = self.input_box.text().strip()
        if not user_text:
            return

        self.append_message("user", user_text)
        self.input_box.clear()

        try:
            response = self.assistant.run(user_text)
        except GroqError as error:
            self.append_message(
                "assistant",
                f"Couldn't get a reply from Groq: {error}",
            )
            return

        self.last_response = response
        self.append_message("assistant", response)

    def listen_voice(self):
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source)
                audio = self.recognizer.listen(source)
                text = self.recognizer.recognize_google(audio)
                self.input_box.setText(text)
        except sr.UnknownValueError:
            pass
        except sr.RequestError:
            pass

    def speak_response(self):
        if hasattr(self, "last_response"):
            self.engine.say(self.last_response)
            self.engine.runAndWait()


if __name__ == "__main__":
    from dotenv import load_dotenv
    import os

    load_dotenv("new.env")
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY is not set in new.env or the environment.")

    app = QApplication([])
    window = ChatApp(LocalAssistant(api_key))
    window.show()
    app.exec()
