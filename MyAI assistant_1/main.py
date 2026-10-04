from PyQt6.QtWidgets import QApplication
from calling import LocalAssistant
from ui import ChatApp
from dotenv import load_dotenv
import os

load_dotenv("new.env")

def main():
    print("Starting MyAI Assistant...")

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("Error: GROQ_API_KEY is not set in the environment variables.")
        return
    assistant = LocalAssistant(api_key)

    app = QApplication([])
    window = ChatApp(assistant)
    window.show()
    app.exec()

if __name__ == "__main__":
    main()
