from agents import Agent
from pydantic import BaseModel
from config import agent_model


QUERY_INSTRUCTIONS = """You are a helpful assistant that can generate search queries for research.
For each request follow these steps:

1. First, think through and explain:
    - Break down the key aspects that need to be researched
    - Consider potential challenges and how you will address them
    - Explain your strategy for finding comprehensive information

2. Then, generate 3 search queries that:
    - Are specific and focused on retrieving high-quality relevant information
    - Cover different aspects of the topic
    - Will help find relevant and diverse information"""

class QueryResponse(BaseModel):
    queries: list[str]
    thoughts: str

query_agent = Agent(
    name = "Query Generator Agent",
    instructions = QUERY_INSTRUCTIONS,
    output_type = QueryResponse,
    model = agent_model
)