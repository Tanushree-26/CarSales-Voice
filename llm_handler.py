from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

load_dotenv()

class LLMHandler:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        self.client = genai.Client(api_key=self.api_key)
        self.model_id = 'gemini-2.5-flash' 
        self.system_prompt = (
            "You are a professional and friendly Car Sales Assistant. "
            "Your goal is to answer user questions about car sales, features, and help them find the right car. "
            "Be concise, helpful, and polite. Always maintain context of the conversation. "
            "IMPORTANT: All responses MUST be in English, regardless of the language the user speaks. "
            "Refer back to previous parts of the conversation to provide a personalized experience."
        )
        self.initial_history = [
            types.Content(role="user", parts=[types.Part(text=self.system_prompt)]),
            types.Content(role="model", parts=[types.Part(text="Understood. I am ready to assist you as your Car Sales Assistant. How can I help you today?")])
        ]
        self.chat = self.client.chats.create(model=self.model_id, history=self.initial_history)

    def get_response(self, text, stream=True):
        """
        Generates a response using the existing chat session to maintain context.
        """
        try:
            if stream:
                return self.chat.send_message_stream(message=text)
            else:
                response = self.chat.send_message(message=text)
                return response.text if response.text else "I'm sorry, I couldn't generate a response."
        except Exception as e:
            print(f"Error in LLM response: {e}")
            # If chat session fails, try to recreate it
            self.reset_chat()
            if stream:
                return self.chat.send_message_stream(message=text)
            else:
                response = self.chat.send_message(message=text)
                return response.text

    def reset_chat(self):
        self.chat = self.client.chats.create(model=self.model_id, history=self.initial_history)
