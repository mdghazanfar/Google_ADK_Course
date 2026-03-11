import warnings
import asyncio
import os
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from dotenv import load_dotenv

warnings.filterwarnings("ignore")

load_dotenv()
# Set API key as environment variable
os.getenv("GOOGLE_API_KEY")

root_agent = Agent(
    model="gemini-2.0-flash-exp",
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


async def main():
    session_service = InMemorySessionService()
    await session_service.create_session(
        app_name="capital-find-app", user_id="user123", session_id="session123"
    )

    runner = Runner(
        agent=root_agent, app_name="capital-find-app", session_service=session_service
    )

    user_input = "What is the capital of Japan?"
    content = types.Content(role="user", parts=[types.Part(text=user_input)])
    events = runner.run(user_id="user123", session_id="session123", new_message=content)

    for event in events:
        if event.is_final_response():
            print(f"Response: {event.content.parts[0].text}")


if __name__ == "__main__":
    asyncio.run(main())
