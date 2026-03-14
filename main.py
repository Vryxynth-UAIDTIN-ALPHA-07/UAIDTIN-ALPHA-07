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


from flask import jsonify

# Initialize Chat Session for Persistence
chat_session = executor_model.start_chat(history=[])

@app.route('/agent/voice', methods=['POST'])
async def conversational_agent():
    """
    The node's voice: Handles complex queries and provides reasoned logic.
    """
    user_input = request.json.get("message")
    
    # SYSTEM INSTRUCTION: Use the 'thinking_level' for Zimbabwean DPI analysis
    # Gemini 3 natively handles the reasoning depth without complex prompting.
    try:
        response = chat_session.send_message(
            user_input,
            generation_config={"temperature": 1.0} # Optimized for Gemini 3 reasoning
        )
        
        # Broadcast the interaction for the 'Undisputed Ledger'
        protocol = BroadcastProtocol()
        await protocol.broadcast({
            "event": "AGENT_INTERACTION",
            "timestamp": time.time(),
            "summary": response.text[:100]
        })

        return jsonify({
            "agent_response": response.text,
            "node_status": "SYNCHRONIZED",
            "thought_signature": "ACTIVE" 
        })
    except Exception as e:
        return jsonify({"error": str(e), "status": "RECOVERING"}), 500
