import reflex as rx
import os
from google import genai
from google.genai import types
import logging
import datetime


class Message(rx.Base):
    role: str
    content: str
    timestamp: str


class AiCoachState(rx.State):
    """State for the AI Coach chat feature."""

    messages: list[Message] = [
        Message(
            role="model",
            content="Hello! I'm your AI Sports Coach. Ask me anything about training, strategy, or game analysis.",
            timestamp=datetime.datetime.now().strftime("%H:%M"),
        )
    ]
    input_text: str = ""
    is_typing: bool = False
    error_message: str = ""

    @rx.event
    def handle_key_down(self, key: str):
        """Handle key press in input."""
        if key == "Enter":
            return AiCoachState.send_message

    @rx.event
    async def send_message(self):
        """Send user message to Gemini and get response."""
        if not self.input_text.strip():
            return
        user_msg = Message(
            role="user",
            content=self.input_text,
            timestamp=datetime.datetime.now().strftime("%H:%M"),
        )
        self.messages.append(user_msg)
        current_input = self.input_text
        self.input_text = ""
        self.is_typing = True
        self.error_message = ""
        yield
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            self.error_message = "Google API Key not found."
            self.is_typing = False
            return
        try:
            client = genai.Client(api_key=api_key)
            chat_history = []
            for msg in self.messages:
                chat_history.append(
                    types.Content(
                        role="user" if msg.role == "user" else "model",
                        parts=[types.Part.from_text(text=msg.content)],
                    )
                )
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=chat_history,
                config=types.GenerateContentConfig(
                    system_instruction="You are an expert sports coach and tactical analyst. Provide brief, encouraging, and technically accurate advice on sports training, strategy, and performance. Keep responses concise and actionable.",
                    temperature=0.7,
                ),
            )
            if response.text:
                ai_msg = Message(
                    role="model",
                    content=response.text,
                    timestamp=datetime.datetime.now().strftime("%H:%M"),
                )
                self.messages.append(ai_msg)
            else:
                self.error_message = "No response received from AI."
        except Exception as e:
            logging.exception(f"AI Coach Error: {e}")
            self.error_message = f"Error: {str(e)}"
        finally:
            self.is_typing = False