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

from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    format="[%(asctime)s - %(name)s:%(lineno)d - %(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filename="driver.log",
    filemode="a",  # Append mode,
    level=logging.DEBUG,  # Set the logging level to DEBUG
)
#logging.getLogger("kernel").setLevel(logging.DEBUG)

def _get_4o_mini() -> AzureChatCompletion:
    return AzureChatCompletion(
        deployment_name="gpt-4o-mini",
        service_id="gpt-4o-mini",
    )
    
def _get_o3_mini() -> AzureChatCompletion:
    return AzureChatCompletion(
        deployment_name="o3-mini",
        service_id="o3-mini",
    )
    
async def main():
    # Initialize the kernel
    kernel = Kernel()

    # Add Azure OpenAI chat completions
    gpt_4o_mini_completion = _get_4o_mini()
    o3_mini_completion = _get_o3_mini()
    
    kernel.add_service(gpt_4o_mini_completion)
    kernel.add_service(o3_mini_completion)
    
    execution_settings = AzureChatPromptExecutionSettings(service_id="o3-mini")
    execution_settings.function_choice_behavior = FunctionChoiceBehavior.Auto()
    
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
        result = await o3_mini_completion.get_chat_message_content(
            chat_history=history,
            settings=execution_settings,
            kernel=kernel,
        )

        # Print the results
        print("Assistant > " + str(result))

        # Add the message from the agent to the chat history
        history.add_message(result)
        

# Run the main function
if __name__ == "__main__":
    asyncio.run(main())