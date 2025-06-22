from flask import Flask, request, jsonify

app = Flask(__name__)

## Define Agent Card
AGENT_CARD = {
    "name": "EchoAgent",
    "description": "A simple agent that echoes back user messages.",
    "url": "http://localhost:5000",
    "version": "1.0",
    "capabilities": {
        "streaming": False,
        "pushNotificcations": False
    }
}

### Agent Card ####
# Serve the Agent Card at the well-known URL
@app.get("/.well-known/agent.json")
def get_agent_card():
    """Endpoint to provide Agent's metadata - Agent Card"""
    return jsonify(AGENT_CARD)

### Task ######
@app.post("/tasks/send")
def handle_task():
    """Endpoint for A2A clients to send a new task"""
    task_request = request.get_json()
    task_id = task_request.get("id")
    user_message = ""
    try:
        user_message = task_request["message"]["parts"][0]["text"]
    except Exception as e:
        return jsonify({"error": "Invalid request format"}), 400
    
    agent_reply_text = f"Hello User, You said: '{user_message}'"

    # Formulate the response in A2A Task format
    response_task = {
        "id": task_id,
        "status": {"state": "completed"},
        "messages": [
            task_request.get("message", {}),
            {
                "role": "agent",
                "parts": [{"text": agent_reply_text}]
            }
        ]
    }
    return jsonify(response_task)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

