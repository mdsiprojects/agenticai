import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import (
    OpenAIChatCompletionsModel,
    ModelProvider,
    Model,
    set_default_openai_client,
    set_default_openai_api,
    set_tracing_disabled,
    set_tracing_export_api_key,
)


def get_openai_client() -> AsyncOpenAI:
    """
    Returns the OpenAI client and sets defaults
    """
    load_dotenv()
    # Set the default OpenAI client with the API key from the environment variable
    client = AsyncOpenAI(
            base_url="https://models.inference.ai.azure.com",
            api_key=os.environ["GITHUB_TOKEN"],
        )

    set_default_openai_client(client)
    set_default_openai_api("chat_completions")
    set_tracing_export_api_key(os.environ["OPENAI_TRACING_KEY"])
    set_tracing_disabled(False)

    return client


def get_github_model_provider(client, model="gpt-4o") -> ModelProvider:
    """
    Returns the model provider
    """
    class GitHubModelProvider(ModelProvider):
        def get_model(self, model_name) -> Model:
            return OpenAIChatCompletionsModel(
                model=model,
                openai_client=client)

    GITHUB_MODEL_PROVIDER = GitHubModelProvider()

    return GITHUB_MODEL_PROVIDER
