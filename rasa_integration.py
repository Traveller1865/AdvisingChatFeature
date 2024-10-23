from rasa.core.agent import Agent
from rasa.shared.utils.io import json_to_string
from rasa.utils.endpoints import EndpointConfig
import asyncio
import os

class RasaChatbot:
    def __init__(self):
        self.agent = None
        self.model_path = "rasa_bot/models"
        self.initialize_agent()

    def initialize_agent(self):
        try:
            self.agent = Agent.load(self.model_path)
        except Exception as e:
            print(f"Error loading Rasa model: {str(e)}")
            self.agent = None

    async def get_response(self, message: str) -> str:
        if not self.agent:
            return "I'm currently experiencing technical difficulties. Please try again later."
        
        try:
            response = await self.agent.handle_text(message)
            if response and len(response) > 0:
                return response[0]['text']
            return "I'm not sure how to respond to that. Would you like to speak with an advisor?"
        except Exception as e:
            print(f"Error getting response from Rasa: {str(e)}")
            return "I'm having trouble understanding. Would you like to speak with an advisor?"

# Create a synchronous wrapper for the async function
def get_bot_response(message: str) -> str:
    bot = RasaChatbot()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    response = loop.run_until_complete(bot.get_response(message))
    loop.close()
    return response
