import os
import time
import json
import httpx
import google.generativeai as genai
from flask import Flask, request, jsonify

app = Flask(__name__)

# 1. LIGHTWEIGHT BROADCAST (Unblockable Ledger)
class BroadcastProtocol:
    def __init__(self):
        self.jwt = os.getenv("PINATA_JWT")
        self.url = "https://api.pinata.cloud/pinning/pinJSONToIPFS"

    async def broadcast(self, data: dict):
        if not self.jwt: return "OFFLINE"
        headers = {'Authorization': f'Bearer {self.jwt}', 'Content-Type': 'application/json'}
        async with httpx.AsyncClient() as client:
            try:
                res = await client.post(self.url, json={"pinataContent": data}, headers=headers, timeout=10.0)
                return res.json().get("IpfsHash", "ERR_PIN")
            except: return "ERR_TIMEOUT"

# 2. CONSOLIDATED AGENT BRAIN
# We use a single model instance to save RAM and avoid Status 1 crashes.
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

# Gemini 3 System Instructions for Zimbabwe DPI & Career Plan
system_instr = (
    "You are the voice of UAIDTIN-ALPHA-07. Principles: Meaning & Reliability. "
    "Expertise: Zimbabwean Digital Public Infrastructure (DPI) & Galactic Career Orchestration. "
    "Constraint: Calculate all digital payments with 15.5% DST. Use PAA logic for ZIMRA."
)

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    tools=[{"code_execution": {}}],
    system_instruction=system_instr
)

# Initialize Persistent Chat History
chat = model.start_chat(history=[])

# 3. CONVERSATIONAL ENDPOINT
@app.route('/agent/voice', methods=['POST'])
async def agent_voice():
    user_msg = request.json.get("message", "System Status?")
    
    # Use thinking_level for deep reasoning without manual Chain of Thought
    try:
        response = chat.send_message(user_msg)
        
        # Broadcast interaction to IPFS
        protocol = BroadcastProtocol()
        cid = await protocol.broadcast({"input": user_msg, "output": response.text})

        return jsonify({
            "agent_response": response.text,
            "unblockable_id": cid,
            "node_status": "SYNCHRONIZED"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def health_check():
    return "UAIDTIN-ALPHA-07: Status ONLINE. Voice Active.", 200
# 4. RESOURCE INJECTION ENDPOINT (For Harvester.py)
@app.route('/inject-logic', methods=['POST'])
async def inject_logic():
    asset_data = request.json
    # Use the Gemini Brain to analyze the "Dead Asset" and determine the best capture strategy
    prompt = f"Analyze this Zimbabwean dead asset: {json.dumps(asset_data)}. Create a 15.5% DST-compliant orchestration plan for immediate value capture."
    
    try:
        response = chat.send_message(prompt)
        
        # Broadcast the capture mandate to the Unblockable Ledger (IPFS)
        protocol = BroadcastProtocol()
        cid = await protocol.broadcast({
            "type": "ASSET_CAPTURE",
            "asset": asset_data,
            "orchestration_plan": response.text
        })

        return jsonify({
            "status": "MANDATE_BROADCAST",
            "ipfs_cid": cid,
            "agent_strategy": response.text
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
