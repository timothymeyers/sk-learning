import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage,AssistantMessage
from azure.core.credentials import AzureKeyCredential

from dotenv import load_dotenv

load_dotenv()
model_name = "Phi-4"

# For Serverless API or Managed Compute endpoints
client = ChatCompletionsClient(
    endpoint="https://phi-4-vtxkl.eastus2.models.ai.azure.com",
    credential=AzureKeyCredential(os.getenv("AZURE_OPENAI_KEY")),
)

response = client.complete(
    stream=True,
    messages=[
        SystemMessage(content="You are a helpful assistant."),
        UserMessage(content="I am going to Paris, what should I see?")
    ],
    max_tokens=2048,
    temperature=0.8,
    top_p=0.1,
    presence_penalty=0.0,
    frequency_penalty=0.0,
    model=model_name
)

for update in response:
    if update.choices:
        print(update.choices[0].delta.content or "", end="")

client.close()