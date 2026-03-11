import os
from dotenv import load_dotenv
import warnings  # Suppress warnings for cleaner output
from google.adk.agents import Agent, ParallelAgent, SequentialAgent
from google.adk.tools.google_search_tool import google_search

warnings.filterwarnings("ignore")

load_dotenv()
os.getenv("GOOGLE_API_KEY")


# news search agent timestamp - timestamp: 1755335715.212168

#
# Multiple search agents running in parallel
web_search_agent = Agent(
    name="web_search_agent",
    model="gemini-2.0-flash",
    description="Searches general web content",
    instruction="Search for general information on the web",
    tools=[google_search],
    output_key="web_results",
)

news_search_agent = Agent(
    name="news_search_agent",
    model="gemini-2.0-flash",
    description="Searches for recent news and updates",
    instruction="Focus on recent news and current events",
    tools=[google_search],  # Could be news-specific tool
    output_key="news_results",
)

academic_search_agent = Agent(
    name="academic_search_agent",
    model="gemini-2.0-flash",
    description="Searches for academic and research content",
    instruction="Focus on scholarly articles and research papers",
    tools=[google_search],  # Could be academic-specific tool
    output_key="academic_results",
)

# Parallel execution of all search agents
parallel_search = ParallelAgent(
    name="parallel_search",
    sub_agents=[web_search_agent, news_search_agent, academic_search_agent],
)

# Updated summary agent to handle multiple sources
comprehensive_summary_agent = Agent(
    name="comprehensive_summary_agent",
    model="gemini-2.0-flash",
    description="Summarizes information from multiple sources",
    instruction="Create a comprehensive summary combining web, news, and academic sources. Highlight different perspectives.",
    output_key="summary",
)

# Create a sequential pipeline that runs parallel search first, then summary
root_agent = SequentialAgent(
    name="parallel_search_pipeline",
    description="Runs parallel searches then creates comprehensive summary",
    sub_agents=[parallel_search, comprehensive_summary_agent],
)
