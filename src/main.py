# import json
# from fastapi import FastAPI, Request

# app = FastAPI()

# # Load keyword-response mappings
# def load_responses():
#     with open("config/responses.json", "r") as file:
#         return json.load(file)

# responses = load_responses()

# @app.post("/webhook")
# async def receive_message(request: Request):
#     data = await request.json()
#     message_text = data.get("message", "").lower()  # Convert message to lowercase
    
#     # Check for a matching keyword
#     for keyword, response in responses.items():
#         if keyword in message_text:
#             return {"response": response}

#     # Default response if no keywords match
#     return {"response": "I'm not sure I understand. Can you clarify?"}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)




import json
import requests
import time
import threading
import logging
from contextlib import asynccontextmanager

from datetime import datetime, timezone
from fastapi import FastAPI, Request

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("auto_responder")


# Load keyword-response mapping from a JSON file
def load_responses():
    try:
        with open("config/responses.json", "r") as file:
            return json.load(file)
    except Exception as e:
        logger.error("Error loading responses.json: %s", e)
        return {}

# Global dictionary to keep track of keyword usage (for demonstration purposes)
usage_log = {}

responses = load_responses()


def keep_alive(url: str, interval: int):
    while True:
        try:
            response = requests.get(url)
            logger.info(f"Reloaded at {datetime.now(timezone.utc).isoformat()}: Status Code {response.status_code}")
        except Exception as e:
            logger.error(f"Error reloading at {datetime.now(timezone.utc).isoformat()}: {str(e)}")
        time.sleep(interval)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: start the keep-alive thread
    keep_alive_url = "https://personalized-auto-responder-1.onrender.com/"  # Replace with your actual Render URL
    thread = threading.Thread(target=keep_alive, args=(keep_alive_url, 30))
    thread.daemon = True  # Ensure thread exits with the application
    thread.start()
    yield
    # Shutdown: perform any cleanup if needed

# Create the FastAPI app with the lifespan context
app = FastAPI(lifespan=lifespan)


@app.post("/webhook")
async def receive_message(request: Request):
    data = await request.json()
    message_text = data.get("message", "").lower()
    sender_name = data.get("sender", "User")  # Optional: use a sender field if available

    selected_response = None

    # Loop through the keyword mappings and check if any keyword is present in the message
    for keyword, response in responses.items():
        if keyword in message_text:
            selected_response = response.replace("[Name]", sender_name)
            # Log the usage: increment count for the keyword
            usage_log[keyword] = usage_log.get(keyword, 0) + 1
            logger.info("Keyword '%s' triggered. Total count: %d", keyword, usage_log[keyword])
            break

    # Use a default fallback response if no keyword is matched
    if not selected_response:
        selected_response = "Could you please clarify what you mean?"

    # Log the entire message received with a timestamp
    logger.info("Received message: %s", data)

    # Return the personalized response
    return {"response": selected_response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=True)
