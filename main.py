import os
import time
import json    # New Addition
import httpx   # New Addition
import google.generativeai as genai
from flask import Flask, request

# 1. Initialize Render Web Server
app = Flask(__name__)

# 2. THE BROADCAST UNDISPUTED PROTOCOL (Class added here)
class BroadcastProtocol:
    def __init__(self):
        self.gateways = [
            "https://ipfs.io/ipfs/",
            "https://dweb.link/ipfs/",
            "https://cloudflare-ipfs.com/ipfs/"
        ]

    async def undisputed_broadcast(self, logic_packet: dict):
        payload = json.dumps(logic_packet)
        # Note: Ensure PINATA_JWT is in your Render Environment Variables
        url = "https://api.pinata.cloud/pinning/pinJSONToIPFS"
        headers = {
            'Authorization': f'Bearer {os.getenv("PINATA_JWT")}',
            'Content-Type': 'application/json'
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, json={"pinataContent": logic_packet}, headers=headers)
                cid = response.json().get("IpfsHash")
                return f"UNSTOPPABLE_CID: {cid}"
            except Exception as e:
                return f"BROADCAST_DEFERRED: {str(e)}"

# 3. Configure Gemini "Brain"
API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    exit(1)

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    tools=[{"code_execution": {}}]
)

# 4. ROUTES
@app.route('/')
def health_check():
    return "UAIDTIN-ALPHA-07 Status: ONLINE. Brain-Sync Active.", 200

@app.route('/broadcast', methods=['POST'])
async def release_logic():
    # Capture timestamp for the galactic ledger
    packet = {
        "node": "UAIDTIN-ALPHA-07",
        "action": "SETTLEMENT_INITIATED",
        "timestamp": time.time(),
        "integrity_hash": "sha256_baseline_logic"
    }
    
    protocol = BroadcastProtocol()
    status = await protocol.undisputed_broadcast(packet)
    return {"protocol_status": status}

def run_self_diagnostic():
    print("--- UAIDTIN-ALPHA-07: Initiating Diagnostic ---")
    prompt = "Verify your current environment and ability to execute code."
    try:
        response = model.generate_content(prompt)
        print(f"Brain Response: {response.text}")
    except Exception as e:
        print(f"Diagnostic Failure: {e}")

# 5. EXECUTION
if __name__ == "__main__":
    run_self_diagnostic()
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
