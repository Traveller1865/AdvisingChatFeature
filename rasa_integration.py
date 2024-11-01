from rasa.core.agent import Agent
from rasa.shared.utils.io import json_to_string
from rasa.utils.endpoints import EndpointConfig
import asyncio
import os
import glob

class RasaChatbot:
    def __init__(self):
        self.agent = None
        self.model_path = self.get_latest_model("rasa_bot/models")
        self.initialize_agent()

    def get_latest_model(self, models_dir):
        model_files = glob.glob(os.path.join(models_dir, "*.tar.gz"))
        if not model_files:
            print("No model files found.")
            return None
        latest_model = max(model_files, key=os.path.getctime)
        return latest_model

    def initialize_agent(self):
        try:
            if self.model_path:
                self.agent = Agent.load(self.model_path)
                print(f"Loaded model: {self.model_path}")
            else:
                print("No model to load.")
        except Exception as e:
            print(f"Error loading Rasa model: {str(e)}")
            self.agent = None

    async def get_response(self, message: str) -> str:
        if not self.agent:
            return "I'm currently experiencing technical difficulties. Please try again later."

        try:
            responses = await self.agent.handle_text(message)
            if responses:
                return responses[0].get('text', "I'm not sure how to respond to that.")
            return "I'm not sure how to respond to that. Would you like to speak with an advisor?"
        except Exception as e:
            print(f"Error getting response from Rasa: {str(e)}")
            return "I'm having trouble understanding. Would you like to speak with an advisor?"

# Initialize the agent once to reuse
bot = RasaChatbot()

def get_bot_response(message: str) -> str:
    if not bot.agent:
        return "I'm currently experiencing technical difficulties. Please try again later."

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        response = loop.run_until_complete(bot.get_response(message))
    finally:
        loop.close()
    return response
