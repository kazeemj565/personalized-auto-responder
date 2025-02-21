import json
from src.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_known_keyword():
    response = client.post("/webhook", json={"message": "hello"})
    assert response.status_code == 200
    assert json.loads(response.text)["response"] == "Hi! How can I help you today?"

def test_unknown_keyword():
    response = client.post("/webhook", json={"message": "unknown phrase"})
    assert response.status_code == 200
    assert json.loads(response.text)["response"] == "I'm not sure I understand. Can you clarify?"
