import os
from dotenv import find_dotenv, load_dotenv
from openai import AsyncOpenAI
from agents import OpenAIChatCompletionsModel


load_dotenv(find_dotenv())

gemini_api_key = os.getenv("GEMINI_API_KEY")

external_client = AsyncOpenAI(
    api_key = gemini_api_key,
    base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
)

agent_model = OpenAIChatCompletionsModel(
    model = "gemini-1.5-flash",
    openai_client = external_client
)