import os
from dotenv import load_dotenv
from tools.weather_utils import WeatherUtils

from semantic_kernel.agents import ChatCompletionAgent, ChatHistoryAgentThread
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion


class WeatherAgent(ChatCompletionAgent):
    
    def __init__(self, 
                 service: AzureChatCompletion,
                 kernel=None,
                 name="WeatherAgent",
                 instructions="You are a helpful assistant that provides weather information.",
                 ):
        super().__init__(service=service,kernel=kernel,name=name, instructions=instructions)
        