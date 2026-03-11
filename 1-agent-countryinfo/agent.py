import warnings
from google.adk.agents import Agent

warnings.filterwarnings("ignore")

root_agent = Agent(
    model="gemini-2.0-flash",
    name="country_capital_agent",
    description="Answers user questions about the capital city of a given country.",
    instruction="""You are an agent that provides the capital city of a country.
                    When a user asks for the capital of a country:
                    1. Identify the country name from the user's query.
                    2. Respond clearly to the user, stating the capital city.
                    Example Query: "What's the capital of France?"
                    Example Response: "The capital of France is Paris."
                    """,
)

__all__ = ["root_agent"]
