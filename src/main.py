import json
import requests
import time
import threading
import logging
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles

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
    thread.daemon = True  
    thread.start()
    yield
    # Shutdown: perform any cleanup if needed

# Create the FastAPI app with the lifespan context
app = FastAPI(lifespan=lifespan)

# Mount the static directory to serve files (e.g., integration JSON)
app.mount("/static", StaticFiles(directory="static"), name="static")

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
            usage_log[keyword] = usage_log.get(keyword, 0) + 1
            logger.info("Keyword '%s' triggered. Total count: %d", keyword, usage_log[keyword])
            break

    # Use a default fallback response if no keyword is matched
    if not selected_response:
        selected_response = "Could you please clarify what you mean?"

    # Log the entire message received with a timestamp
    logger.info("Received message: %s", data)

    return {"response": selected_response}

# @app.get("/")
# def read_root():
#     return {"message": "Welcome to the Personalized Auto-Responder!"}


# GET route for a descriptive landing page (shows integration details)
@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <html>
      <head>
        <title>Personalized Auto-Responder</title>
        <style>
          body { font-family: Arial, sans-serif; margin: 40px; background-color: #f4f4f4; }
          .container { background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
          h1 { color: #1A73E8; }
          ul { line-height: 1.6; }
        </style>
      </head>
      <body>
        <div class="container">
          <h1>Personalized Auto-Responder</h1>
          <p>This integration automatically detects predefined keywords in incoming Telex channel messages and sends personalized text responses to enhance team communication.</p>
          <p><strong>Key Features:</strong></p>
          <ul>
            <li>Real-time keyword detection</li>
            <li>Personalized responses using sender information</li>
            <li>Customizable via JSON configuration</li>
            <li>Usage logging for performance refinement</li>
          </ul>
          <p>To integrate this app, ensure that your channel messages are routed to our webhook endpoint:</p>
          <p><code>https://personalized-auto-responder-1.onrender.com/webhook</code></p>
        </div>
      </body>
    </html>
    """

if __name__ == "__main__":
    import uvicorn
    import os

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)





