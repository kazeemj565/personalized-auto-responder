# Personalized Auto-Responder Integration for Telex

Below is a sample **README.md** for your **Personalized Auto-Responder** project. It covers the project overview, setup instructions, testing, deployment, and details on integrating with Telex. Feel free to modify any section to match your exact workflow or preferences.

---

# Personalized Auto-Responder

This **Modifier Integration** for Telex automatically detects predefined keywords in incoming Telex channel messages and responds with personalized text. It enhances team communication by providing immediate, context-aware replies.

## Table of Contents

1. [Overview](#overview)  
2. [Features](#features)  
3. [Requirements](#requirements)  
4. [Local Setup](#local-setup)  
   - [Installation](#installation)  
   - [Configuration](#configuration)  
   - [Running Locally](#running-locally)  
5. [Testing](#testing)  
6. [Deployment to Render](#deployment-to-render)  
7. [Hosting the Integration JSON](#hosting-the-integration-json)  
8. [Integrating with Telex](#integrating-with-telex)  
9. [Contributing](#contributing)  
10. [License](#license)

---

## Overview

The **Personalized Auto-Responder** is a Telex integration designed to automatically reply to incoming channel messages based on keyword detection. It’s built with **FastAPI** and uses a simple JSON file for mapping keywords to responses. When installed as a **Modifier Integration** in Telex, it intercepts new messages and modifies them before they’re displayed in the channel.

### How It Works

1. **Telex sends a POST request** to this integration’s `/webhook` endpoint whenever a new message arrives.  
2. The integration **analyzes the message** to find known keywords.  
3. If a keyword is detected, it **returns a personalized response** (e.g., greeting the sender by name).  
4. If no keywords match, a **fallback** response is sent.

---

## Features

- **Keyword Detection**: Detects keywords like “hello”, “help”, or “thanks”.  
- **Personalized Replies**: Injects the sender’s name into responses.  
- **Configurable via JSON**: `responses.json` allows easy updates to keyword mappings.  
- **Usage Logging**: Logs each keyword trigger for future optimization.  
- **Keep-Alive Mechanism**: (Optional) Pings the hosted app so it doesn’t spin down on Render.

---

## Requirements

- **Python 3.8+**  
- **FastAPI** & **Uvicorn**  
- **Git** for version control  
- (Optional) **Render** account for deployment  
- (Optional) **Telex** account to install and test the integration

---

## Local Setup

### Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/<your-username>/personalized-auto-responder.git
   cd personalized-auto-responder
   ```

2. **Create a Virtual Environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   # or:
   venv\Scripts\activate     # On Windows
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Configuration

1. **Keyword Mappings**:  
   Update `config/responses.json` with your desired keywords and responses. For example:
   ```json
   {
     "hello": "Hi [Name]! How can I help you today?",
     "help": "I'm here to help! What do you need assistance with?",
     "thanks": "You're welcome! Let me know if you need anything else."
   }
   ```

2. **Integration JSON**:  
   The file `static/integration.json` describes your integration for Telex. Make sure `target_url` matches your deployed URL (e.g., `https://personalized-auto-responder-1.onrender.com/webhook`).

### Running Locally

```bash
uvicorn src.main:app --reload --port 8000
```

- **Visit**: `http://localhost:8000/`  
- **Test the Webhook**:
  ```bash
  curl -X POST "http://localhost:8000/webhook" \
       -H "Content-Type: application/json" \
       -d '{"message": "hello", "sender": "Alice"}'
  ```

You should see a response like:
```json
{"response": "Hi Alice! How can I help you today?"}
```

---

## Testing

We use **pytest** for unit tests. Example:

```bash
pytest tests/
```

- **`tests/test_responder.py`** checks that known keywords trigger the correct responses, and unknown text yields the fallback message.
- Ensure **httpx** is installed if needed by FastAPI’s `TestClient`.

---

## Deployment to Render

1. **Create a New Web Service** on Render:
   - Connect to your GitHub repo.
   - Use the build command (e.g., `pip install -r requirements.txt`).
   - Use the run command: `uvicorn src.main:app --host 0.0.0.0 --port $PORT`.
2. **Automatic Deployment**:  
   - Each push to `main` triggers a build.
3. **Check Logs**:  
   - In the Render dashboard, verify your app starts with no errors.
   - Confirm it’s listening on the correct port.

**Keep-Alive**: We included a background thread that periodically pings the Render URL so the service stays awake.

---

## Hosting the Integration JSON

We serve `integration.json` via FastAPI’s static files:

- **Static Mount**:
  ```python
  from fastapi.staticfiles import StaticFiles
  app.mount("/static", StaticFiles(directory="static"), name="static")
  ```
- Place `integration.json` (and any logo images) in `static/`.  
- Public URL example:
  ```
  https://personalized-auto-responder-1.onrender.com/static/integration.json
  ```
  
This file includes your `app_name`, `app_logo`, `integration_type`, and `target_url`.

---

## Integrating with Telex

1. **Obtain the Hosted JSON URL**:
   - For example: `https://personalized-auto-responder-1.onrender.com/static/integration.json`.
2. **Open Telex**:
   - Go to your workspace or test organization.
   - In “Integrations” (or “Manage Apps”), look for an “Add Integration” or “Add New” button.
3. **Submit the URL**:
   - Paste the public link to `integration.json`.
   - Telex fetches your config and creates a new integration entry.
4. **Enable & Test**:
   - Enable the integration in the desired channel.
   - Send a message like “hello” in that channel. Telex will POST to your `/webhook` route, and your auto-responder should reply with the configured message.

---

## Contributing

1. **Fork** this repo and create a new branch for your feature or bug fix.  
2. **Commit** your changes with meaningful commit messages following [Conventional Commits](https://www.conventionalcommits.org/).  
3. **Open a Pull Request** against the main branch.

---

## License

This project is licensed under the [MIT License](LICENSE). You’re free to modify and distribute as needed.

---

### Questions or Feedback?

Feel free to open an issue or reach out if you have any questions about setup, deployment, or customization of this Personalized Auto-Responder for Telex.