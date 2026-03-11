import asyncio
import os
from dotenv import load_dotenv
import datetime
import logging
import warnings
from zoneinfo import ZoneInfo
from google.adk.agents import Agent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai.types import Content, Part

# Configure logging to see ADK logs
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

load_dotenv()
os.getenv("GOOGLE_API_KEY")  # Ensure the environment variable is loaded

warnings.filterwarnings(
    "ignore",
    message='Field name "config_type" in "SequentialAgent" shadows an attribute in parent "BaseAgent"',
)


def get_weather(city: str) -> dict:
    """Retrieves the current weather report for a specified city.

    Args:
        city (str): The name of the city for which to retrieve the weather report.

    Returns:
        dict: status and result or error msg.
    """
    if city.lower() == "new york":
        return {
            "status": "success",
            "report": (
                "The weather in New York is sunny with a temperature of 25 degrees"
                " Celsius (77 degrees Fahrenheit)."
            ),
        }
    else:
        return {
            "status": "error",
            "error_message": f"Weather information for '{city}' is not available.",
        }


def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city.

    Args:
        city (str): The name of the city for which to retrieve the current time.

    Returns:
        dict: status and result or error msg.
    """

    if city.lower() == "new york":
        tz_identifier = "America/New_York"
    else:
        return {
            "status": "error",
            "error_message": (f"Sorry, I don't have timezone information for {city}."),
        }

    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now(tz)
    report = f'The current time in {city} is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}'
    return {"status": "success", "report": report}


root_agent = Agent(
    name="weather_time_agent",
    model="gemini-2.0-flash",
    description=("Agent to answer questions about the time and weather in a city."),
    instruction=(
        "You are a helpful agent who can answer user questions about the time and weather in a city."
    ),
    tools=[get_weather, get_current_time],
)


async def main():
    print("Starting main function...", flush=True)
    logger.info("Main function started")
    try:
        app_name, user_id, session_id = "weather_time_agent-app", "user1", "session1"
        session_service = InMemorySessionService()
        runner = Runner(
            agent=root_agent, app_name=app_name, session_service=session_service
        )
        session = await session_service.create_session(
            app_name=app_name, user_id=user_id, session_id=session_id
        )
        print(f"Session created for user: {user_id}", flush=True)
        print(f"Session ID: {session_id}", flush=True)
        print(f"App name: {app_name}", flush=True)
        print(f"Initial state: {session.state}", flush=True)
        logger.info(f"Session created: {session_id} for user: {user_id}")

        print(
            f"\nStarting interaction with user: {user_id} in session: {session_id}",
            flush=True,
        )
        logger.info(f"Starting agent interaction")
        user_message = Content(parts=[Part(text="Hello")])
        for event in runner.run(
            user_id=user_id, session_id=session_id, new_message=user_message
        ):
            print(f"Event: {event}", flush=True)
            logger.info(f"Received event: {type(event).__name__}")
            if event.is_final_response():
                print(f"Agent responded: {event.content}", flush=True)
                logger.info("Final response received")

        print(f"\nSession interaction completed for user: {user_id}", flush=True)
        logger.info("Session interaction completed")
    except Exception as e:
        print(f"Error: {e}", flush=True)
        logger.error(f"Error occurred: {e}", exc_info=True)


if __name__ == "__main__":
    print("Script started", flush=True)
    logger.info("Script execution started")
    try:
        asyncio.run(main())
    except PermissionError as e:
        print(f"Permission error: {e}", flush=True)
        # Try alternative approach
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(main())
        loop.close()
    print("Script completed", flush=True)
    logger.info("Script execution completed")
