import os
import time
import json
import httpx
import google.generativeai as genai
from flask import Flask, request, jsonify

app = Flask(__name__)

# 1. LIGHTWEIGHT BROADCAST
class BroadcastProtocol:
    def __init__(self):
        self.jwt = os.getenv("PINATA_JWT")
        self.url = "https://api.pinata.cloud/pinning/pinJSONToIPFS"

    async def broadcast(self, data: dict):
        if not self.jwt: return "NO_JWT"
        headers = {'Authorization': f'Bearer {self.jwt}', 'Content-Type': 'application/json'}
        async with httpx.AsyncClient() as client:
            try:
                res = await client.post(self.url, json={"pinataContent": data}, headers=headers, timeout=10.0)
                return res.json().get("IpfsHash", "ERROR")
            except:
                return "TIMEOUT"

# 2. CONSOLIDATED BRAIN (Saves RAM)
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)
# One model to rule them all
shared_model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    tools=[{"code_execution": {}}]
)

# 3. THE AGENTIC LOOP
@app.route('/orchestrate', methods=['POST'])
async def agentic_loop():
    data = request.get_json() or {}
    goal = data.get("goal", "System check")
    
    # The 'Voice' and 'Muscle' now happen in one sequence
    prompt = f"As the Orchestrator of UAIDTIN-ALPHA-07, execute this goal: {goal}"
    response = shared_model.generate_content(prompt)
    
    # Background broadcast
    protocol = BroadcastProtocol()
    cid = await protocol.broadcast({"goal": goal, "result": response.text})
    
    return jsonify({
        "status": "GOAL_ACHIEVED",
        "unblockable_id": cid,
        "output": response.text
    })

@app.route('/')
def health_check():
    return "UAIDTIN-ALPHA-07: Status ONLINE. Agentic Architecture: READY.", 200

if __name__ == "__main__":
    # Ensure port is handled correctly for Render
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
