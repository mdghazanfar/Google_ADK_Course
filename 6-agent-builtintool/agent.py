import warnings
import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.tools import google_search
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

warnings.filterwarnings(
    "ignore",
    message='Field name "config_type" in "SequentialAgent" shadows an attribute in parent "BaseAgent"',
)

load_dotenv()
os.getenv("GOOGLE_API_KEY")

APP_NAME = "search_agent_app"
USER_ID = "user123"
SESSION_ID = "s1234"

root_agent = Agent(
    name="search_agent",
    model="gemini-2.0-flash",
    description="An agent that provides information by performing search on google using google search tool.",
    instruction="I can answer your questions by searching the internet. Ask me any thing",
    tools=[google_search],
)


# Session and Runner
async def setup_session_and_runner():
    session_service = InMemorySessionService()

    # Check if session already exists
    try:
        existing_session = await session_service.get_session(
            app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
        )
        print(f"Using existing session: {existing_session.session_id}")
        session = existing_session
    except:
        # Create new session with explicit ID
        session = await session_service.create_session(
            app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
        )
        print(f"Created new session: {session.session_id}")

    # Verify the session ID matches what we expect
    if session.session_id != SESSION_ID:
        print(
            f"WARNING: Expected session ID '{SESSION_ID}' but got '{session.session_id}'"
        )
    else:
        print(f"SUCCESS: Session ID matches: {SESSION_ID}")

    runner = Runner(
        agent=root_agent, app_name=APP_NAME, session_service=session_service
    )
    return session, runner


async def main():
    print(f"Configuring session with ID: {SESSION_ID}")
    session, runner = await setup_session_and_runner()
    print(f"Final session details:")
    print(f"  App Name: {session.app_name}")
    print(f"  User ID: {session.user_id}")
    print(f"  Session ID: {session.session_id}")
    print(f"  State: {session.state}")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
