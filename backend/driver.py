import asyncio, os, logging

from semantic_kernel import Kernel
from semantic_kernel.utils.logging import setup_logging
from semantic_kernel.functions import kernel_function

from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.connectors.ai.azure_ai_inference import AzureAIInferenceChatCompletion

from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
from semantic_kernel.connectors.ai.chat_completion_client_base import ChatCompletionClientBase
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.functions.kernel_arguments import KernelArguments
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential

from semantic_kernel.connectors.ai.open_ai.prompt_execution_settings.azure_chat_prompt_execution_settings import (
    AzureChatPromptExecutionSettings,
)

endpoint = "https://oai-tmm-eastus2.openai.azure.com/openai/deployments/gpt-4o-mini/chat/completions?api-version=2025-01-01-preview"
model_name = "gpt-4o-mini"
deployment = "gpt-4o-mini"
api_key = os.getenv("AZURE_OPENAI_KEY")
phi_key = os.getenv("AZURE_PHI_KEY")


logging.basicConfig(
    format="[%(asctime)s - %(name)s:%(lineno)d - %(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logging.getLogger("kernel").setLevel(logging.DEBUG)

async def main():
    # Initialize the kernel
    kernel = Kernel()

    # Add Azure OpenAI chat completion
    chat_completion = AzureChatCompletion(
        deployment_name=deployment,
        api_key=api_key,
        base_url=endpoint,
        service_id="gpt-4o-mini",
    )   
    kernel.add_service(chat_completion)

    phi_chat_completion = AzureAIInferenceChatCompletion(
        ai_model_id="Phi-4",
        api_key=phi_key,
        endpoint="https://phi-4-vtxkl.eastus2.models.ai.azure.com",
        service_id="phi-4",      
    )
    kernel.add_service(phi_chat_completion)

    o3_chat = AzureChatCompletion(
        deployment_name="o3-mini",
        api_key=api_key,
        base_url="https://oai-tmm-eastus2.openai.azure.com/openai/deployments/o3-mini/chat/completions?api-version=2025-01-01-preview",
        service_id="o3-mini",
    )   
    kernel.add_service(o3_chat)

    # Set the logging level for semantic_kernel.kernel to DEBUG.
    setup_logging()
    logging.getLogger("kernel").setLevel(logging.DEBUG)

    # Add a plugin (the LightsPlugin class is defined below)
    kernel.add_plugin(
        LightsPlugin(),
        plugin_name="Lights",
    )

    # Enable planning
    execution_settings = AzureChatPromptExecutionSettings(service_id="o3-mini")
    execution_settings.function_choice_behavior = FunctionChoiceBehavior.Auto()

    # Create a history of the conversation
    history = ChatHistory()

    # Initiate a back-and-forth chat
    userInput = None
    while True:
        # Collect user input
        userInput = input("User > ")

        # Terminate the loop if the user says "exit"
        if userInput == "exit":
            break

        # Add user input to the history
        history.add_user_message(userInput)

        # Get the response from the AI
        result = await chat_completion.get_chat_message_content(
            chat_history=history,
            settings=execution_settings,
            kernel=kernel,
        )

        # Print the results
        print("Assistant > " + str(result))

        # Add the message from the agent to the chat history
        history.add_message(result)


from typing import Annotated
from semantic_kernel.functions import kernel_function

class LightsPlugin:
    lights = [
        {"id": 1, "name": "Table Lamp", "is_on": False},
        {"id": 2, "name": "Porch light", "is_on": False},
        {"id": 3, "name": "Chandelier", "is_on": True},
    ]

    @kernel_function(
        name="get_lights",
        description="Gets a list of lights and their current state",
    )
    def get_state(
        self,
    ) -> str:
        """Gets a list of lights and their current state."""
        return self.lights

    @kernel_function(
        name="change_state",
        description="Changes the state of the light",
    )
    def change_state(
        self,
        id: int,
        is_on: bool,
    ) -> str:
        """Changes the state of the light."""
        for light in self.lights:
            if light["id"] == id:
                light["is_on"] = is_on
                return light
        return None


# Run the main function
if __name__ == "__main__":
    asyncio.run(main())