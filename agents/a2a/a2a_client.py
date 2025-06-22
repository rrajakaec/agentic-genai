import requests
import uuid

# 1. Discover the agent by fetching its Agent Card
AGENT_BASE_URL = "http://localhost:5000"
agent_card_url = f"{AGENT_BASE_URL}/.well-known/agent.json"

response = requests.get(agent_card_url)
if response.status_code != 200:
    raise RuntimeError(f"Failed to get Agent card: {response.status_code}")

agent_card = response.json()
print(f"Discovered Agent:", agent_card)

# 2. Prepare a task request for the agent
task_id = str(uuid.uuid4())
user_text = "What is A2A protocol"

task_payload = {
    "id": task_id,
    "message": {
        "role": "user",
        "parts": [
            {"text": user_text}
        ]
    }
}

# 3. Send the request to the Agent Server tasks/send
tasks_send_url = f"{AGENT_BASE_URL}/tasks/send"
result = requests.post(tasks_send_url, json=task_payload)
if result.status_code != 200:
    raise RuntimeError(f"Error while calling agent's task url: {result.status_code}")
task_response = result.json()

# 4. Process the Agent response
if task_response.get("status", {}).get("state") == "completed":
    messages = task_response.get("messages", [])
    if messages:
        agent_message = messages[-1]
        print(f"Agent Message: {agent_message}")
    else:
        print("No message in response!")
else:
    print("Task did not complete. Status: ", task_response.get("status"))


