import warnings
import os
from dotenv import load_dotenv
from google.adk.agents import Agent, SequentialAgent, LoopAgent
from google.adk.tools.tool_context import ToolContext
from google.adk.tools import google_search

warnings.filterwarnings("ignore")

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


# --- Tool Definition ---
def exit_loop(tool_context: ToolContext):
    """Call this function ONLY when the critique indicates no further changes are needed, signaling the iterative process should end."""
    print(f"  [Tool Call] exit_loop triggered by {tool_context.agent_name}")
    tool_context.actions.escalate = True
    return {}


critic_agent = Agent(
    name="critic_agent",
    model="gemini-2.0-flash",
    description="An agent that critiques the summary provided by the summary agent.",
    instruction="Critique the summary provided by the summary agent. Provide feedback on its accuracy and completeness.",
    tools=[exit_loop],  # Include exit tool to end the loop
    output_key="critique",
)


# STEP 2: Refinement Loop Agent
refinement_loop = LoopAgent(
    name="RefinementLoop",
    # Agent order is crucial: Critique first, then Refine/Exit
    sub_agents=[summary_agent, critic_agent],
    max_iterations=5,  # Limit loops
)


root_agent = SequentialAgent(
    name="text_summarize_pipeline_with_loop",
    description="A pipeline that summarizes text using the summary agent with a refinement loop and"
    " exits once critic feel no other iteration is required.",
    sub_agents=[search_agent, refinement_loop],
)
