import json
from fastapi import FastAPI, Request

app = FastAPI()

# Load keyword-response mappings
def load_responses():
    with open("config/responses.json", "r") as file:
        return json.load(file)

responses = load_responses()

@app.post("/webhook")
async def receive_message(request: Request):
    data = await request.json()
    message_text = data.get("message", "").lower()  # Convert message to lowercase
    
    # Check for a matching keyword
    for keyword, response in responses.items():
        if keyword in message_text:
            return {"response": response}

    # Default response if no keywords match
    return {"response": "I'm not sure I understand. Can you clarify?"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
