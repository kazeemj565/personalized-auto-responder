import json
from src.main import app, responses, usage_log
from fastapi.testclient import TestClient

# Configure test responses to avoid external file dependency
test_responses = {
    "hello": "Hi! How can I help you today?",
    "bye": "Goodbye, [Name]!"
}

# Override the loaded responses with test data
responses.clear()
responses.update(test_responses)

client = TestClient(app)

def test_known_keyword():
    response = client.post("/webhook", json={"message": "hello"})
    assert response.status_code == 200
    assert response.json()["message"] == "Hi! How can I help you today?"

def test_unknown_keyword():
    response = client.post("/webhook", json={"message": "unknown phrase"})
    assert response.status_code == 200
    assert response.json()["message"] == "Could you please clarify what you mean?"

def test_case_insensitivity():
    # Test uppercase message should still match lowercase keyword
    response = client.post("/webhook", json={"message": "HELLO"})
    assert response.status_code == 200
    assert response.json()["message"] == "Hi! How can I help you today?"

def test_name_substitution():
    # Test sender name replacement in response
    response = client.post("/webhook", json={"message": "bye", "sender": "Alice"})
    assert response.status_code == 200
    assert response.json()["message"] == "Goodbye, Alice!"

def test_default_sender_name():
    # Test default "User" when sender not provided
    response = client.post("/webhook", json={"message": "bye"})
    assert response.status_code == 200
    assert response.json()["message"] == "Goodbye, User!"

def test_empty_message():
    # Test empty message handling
    response = client.post("/webhook", json={"message": ""})
    assert response.status_code == 200
    assert response.json()["message"] == "Could you please clarify what you mean?"

def test_missing_message_key():
    # Test request without message field
    response = client.post("/webhook", json={})
    assert response.status_code == 200
    assert response.json()["message"] == "Could you please clarify what you mean?"

def test_usage_log_increment():
    # Reset usage log before test
    usage_log.clear()
    
    # First trigger
    client.post("/webhook", json={"message": "hello"})
    assert usage_log.get("hello") == 1
    
    # Second trigger
    client.post("/webhook", json={"message": "hello"})
    assert usage_log.get("hello") == 2