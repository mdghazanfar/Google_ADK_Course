import warnings
import os
from dotenv import load_dotenv
from google.adk.agents import Agent, SequentialAgent, LlmAgent
from google.adk.types import types
from google.adk.constants import USER_ID, APP_NAME, SESSION_ID_SCHEMA_AGENT
from google.adk.sessions import session_service
import json
from google.adk.tools import google_search
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

warnings.filterwarnings(
    "ignore",
    message='Field name "config_type" in "SequentialAgent" shadows an attribute in parent "BaseAgent"',
)

load_dotenv()
os.getenv("GOOGLE_API_KEY")

search_agent = Agent(
    name="search_agent",
    model="gemini-2.0-flash",
    description="An agent that provides information by performing search on google using google search tool.",
    instruction="I can answer your questions by searching the internet. Ask me any thing",
    tools=[google_search],
    output_key="search_results",
)

summary_agent = Agent(
    name="summary_agent",
    model="gemini-2.0-flash",
    description="An agent that summarizes the search results using the search-agent.",
    instruction="Summarize the given information in two or three lines.",
    output_key="summary",
)


text_summarize_pipeline = SequentialAgent(
    name="text_summarize_pipeline",
    description="A pipeline that summarizes text using the summary agent.",
    sub_agents=[search_agent, summary_agent],
)

root_agent = text_summarize_pipeline

__all__ = ["root_agent"]
