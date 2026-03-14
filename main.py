import os
import time
import json
import httpx
import google.generativeai as genai
from flask import Flask, request

# 1. Initialize Render Web Server
app = Flask(__name__)

# 2. Broadcast Protocol (The Unblockable Channel)
class BroadcastProtocol:
    def __init__(self):
        self.url = "https://api.pinata.cloud/pinning/pinJSONToIPFS"
        self.headers = {
            'Authorization': f'Bearer {os.getenv("PINATA_JWT")}',
            'Content-Type': 'application/json'
        }

    async def broadcast(self, data: dict):
        async with httpx.AsyncClient() as client:
            try:
                res = await client.post(self.url, json={"pinataContent": data}, headers=self.headers)
                return res.json().get("IpfsHash")
            except:
                return "BROADCAST_DEFERRED"

# 3. Configure the "Dual-Role" Brain
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

# Executor: Armed with code_execution tools
executor_model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    tools=[{"code_execution": {}}]
)

# Orchestrator: Pure reasoning (No tools, to prevent loop-confusion)
orchestrator_model = genai.GenerativeModel(model_name="gemini-1.5-flash")

# 4. Agentic Architecture: The Orchestrator vs. Executor Loop
@app.route('/orchestrate', methods=['POST'])
async def agentic_loop():
    user_goal = request.json.get("goal", "Verify system integrity")
    
    # PHASE 1: ORCHESTRATION (The Plan)
    plan_prompt = f"Goal: {user_goal}. Break this into 3 specific Python-executable steps. Output ONLY a JSON list of strings."
    plan_response = orchestrator_model.generate_content(plan_prompt)
    
    # PHASE 2: EXECUTION (The Muscle)
    results = []
    # Simplified loop for mobile-orchestration stability
    execution_prompt = f"Execute this logic and return the final data: {plan_response.text}"
    final_output = executor_model.generate_content(execution_prompt)
    
    # PHASE 3: BROADCAST (The Ledger)
    protocol = BroadcastProtocol()
    cid = await protocol.broadcast({"goal": user_goal, "output": final_output.text})
    
    return {
        "node": "UAIDTIN-ALPHA-07",
        "status": "GOAL_ACHIEVED",
        "unblockable_id": cid,
        "ai_analysis": final_output.text
    }

@app.route('/')
def health_check():
    return "UAIDTIN-ALPHA-07 Status: ONLINE. Agentic Architecture: ACTIVE.", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
